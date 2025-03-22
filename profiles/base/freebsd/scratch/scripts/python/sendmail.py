#!/usr/bin/env python
r"""A simple mail(1) clone implemented in python using builtin libraries.

The script punts emails across the wire until an EOF on stdin is reached. This script
is best used with FIFOs/pipes.

Example:
    echo 'hello world!' | \
        sendmail.py -S sender@domain.com -m your-smtp-host.email-domain.com -p 587 \
            -u SMTP-username -s 'Subject line'

Enji Cooper, October 2013

"""

from __future__ import annotations

import argparse
import getpass
import logging
import pathlib
import select
import smtplib
import socket
import sys
import time
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import os

DEBUG = False
logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s", level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@dataclass
class ServerSettings:
    """Mail server settings."""

    hostname: str
    port: int
    user: str | None
    password: str | None


def add_attachments(attachment_files: list[os.PathLike]) -> list[MIMEText]:
    """Create MIME compatible attachments.

    Args:
        attachment_files: attachments to convert to a MIME-compatible format.

    Returns:
        A MIME-formatted list of attachments.

    """
    attachments = []
    for attachment_file in attachment_files:
        attachment_path = pathlib.Path(attachment_file)
        with attachment_path.open("rb") as attachment_fp:
            attachment = MIMEText(attachment_fp.read(), _charset="utf-8")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment_path.name,
        )
        attachments.append(attachment)
    return attachments


def compose_email(
    sender_email: str,
    recipients: list[str],
    subject: str,
    message: str,
    attachments: list[os.PathLike] | None = None,
) -> str:
    """Compose an email that can be sent via smtplib."""
    if attachments:
        email = MIMEMultipart()
        email.preamble = message
        for attachment in attachments:
            email.attach(attachment)
    else:
        email = MIMEText(message, _charset="utf-8")
    email["From"] = sender_email
    email["To"] = ", ".join(recipients)
    email["Date"] = formatdate()
    email["Subject"] = subject

    return email


def send_email(
    composed_email: str,
    server_settings: ServerSettings,
) -> None:
    """Send an email.

    Args:
        composed_email: an email produced by `composed_email`, which can be ingested
                        by `smtplib`.
        server_settings: settings for mailserver relay.

    """
    smtp_args = []
    if server_settings.hostname:
        smtp_args.append(server_settings.hostname)
        if server_settings.port:
            smtp_args.append(server_settings.port)

    server = smtplib.SMTP(*smtp_args, timeout=10)

    try:
        if DEBUG:
            server.set_debuglevel(1)
        server.ehlo()
        if server.has_extn("STARTTLS"):
            server.starttls()

        try:
            if server_settings.password:
                server.login(server_settings.user, server_settings.password)
        except Exception:
            LOGGER.exception(
                "Could not log in to server with username = %r", server_settings.user,
            )
            raise
        else:
            res = server.send_message(composed_email)
            if LOGGER.isEnabledFor(logging.DEBUG):
                if res:
                    LOGGER.error("Error sending mail: %r", res)
                else:
                    LOGGER.info("Email sent successfully!")
    finally:
        server.quit()


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--server",
        default="localhost",
        dest="server_host",
        help="mail server to use for relaying email.",
    )
    parser.add_argument(
        "-p",
        "--server-port",
        default=socket.getservbyname("smtp"),
        dest="server_port",
        type=int,
        help="port to connect to SMTP on (default: %default).",
    )
    parser.add_argument(
        "-s",
        "--subject",
        dest="subject",
        required=True,
        help="subject line for email.",
    )
    parser.add_argument(
        "-S",
        "--sender",
        default=f"{getpass.getuser()}@{socket.gethostname()}",
        dest="sender_email",
        required=True,
        help="sender's email address (default: %default).",
    )
    parser.add_argument(
        "-u",
        "--server-username",
        dest="server_username",
        help=("mail server user. This can be an email address, shortname, etc."),
    )
    parser.add_argument("recipients", nargs="+", help="email recipients")

    args = parser.parse_args(args=argv)

    mailserver_password = (
        None if args.server_username is None else getpass.getpass("Email password> ")
    )

    server_settings = ServerSettings(
        hostname=args.server_host,
        port=args.server_port,
        user=args.server_username,
        password=mailserver_password,
    )

    rlist = [sys.stdin]

    while True:
        ready = select.select(rlist, [], [])
        msg = ready[0][0].read()
        if msg:
            email_message = compose_email(
                sender_email=args.sender_email,
                recipients=args.recipients,
                subject=args.subject,
                message=msg,
            )
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug("Composed email: %s", email_message)

            send_email(
                composed_email=email_message,
                server_settings=server_settings,
            )
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()
