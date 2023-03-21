#!/usr/bin/env python
"""
A dumb script that sits and punts emails across the wire in a while(1)
manner. Best used with FIFOs.

Sort of ripped from FreeNAS 8 (gui.common.system).

Example:

echo 'hello world!' | \
     python sendmail.py -d gmail.com -m mail.zonarsystems.com -p 587 \
                        -s 'Hello world'

Enji Cooper, October 2013
"""

import argparse
import getpass
import logging
import os
import select
import smtplib
import socket
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import Optional


DEBUG = False


def add_attachments(attachment_files: list[os.PathLike]) -> list[MIMEText]:
    attachments = []
    for attachment_file in attachment_files:
        with open(attachment_file, "rb") as attachment_fp:
            attachment = MIMEText(attachment_fp.read(), _charset="utf-8")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(attachment_file),
        )
        attachments.append(attachment)
    return attachments


def do_email(
    mailserver: str,
    port: int,
    user: str,
    domain: str,
    password: str,
    recipients: list[str],
    message: str,
    subject: str,
    attachments: Optional[os.PathLike] = None,
):
    smtp_args = []
    if mailserver:
        smtp_args.append(mailserver)
        if port:
            smtp_args.append(port)

    user = user or getpass.getuser()
    domain = domain or socket.gethostname()

    server = smtplib.SMTP(*smtp_args, timeout=10)
    try:
        if DEBUG:
            server.set_debuglevel(1)
        server.ehlo()
        if server.has_extn("STARTTLS"):
            server.starttls()

        sender = "@".join([user, domain]).encode("utf-8")

        if attachments:
            msg = MIMEMultipart()
            msg.preamble = message
            for attachment in attachments:
                msg.attach(attachment)
        else:
            msg = MIMEText(message, _charset="utf-8")
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Date"] = formatdate()
        msg["Subject"] = subject
        msg = msg.as_string()

        try:
            if password:
                server.login(user, password)
        except Exception:
            logging.exception("Error logging into server")
            # time.sleep(10)
        res = server.sendmail(sender, recipients, msg)
        if DEBUG:
            if res:
                print(f"Error sending mail: {res!r}")
            else:
                print(f"Email sent!\n{msg}")
    finally:
        server.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        default=".".join(socket.getfqdn().split(".")[1:]),
        dest="sender_domain",
        help=("domain name to use for sender email " "(default: %default)"),
    )
    parser.add_argument(
        "-m",
        default="localhost",
        dest="mailserver",
        help="mailserver to use for relaying email",
    )
    parser.add_argument(
        "-p",
        default=socket.getservbyname("smtp"),
        dest="port",
        type=int,
        help="port to connect to SMTP on (default: %default)",
    )
    parser.add_argument(
        "-s",
        dest="subject",
        help="subject line in email to send",
    )
    parser.add_argument(
        "-u",
        default=os.getenv("USER"),
        dest="sender_user",
        help=("username to use when sending mail " "(default: %default)"),
    )
    parser.add_argument("recipients", nargs="+")

    args = parser.parse_args()

    password = os.getenv("PASSWORD") or getpass.getpass()
    password = password.strip().encode("utf-8")

    rlist = [sys.stdin]

    while True:
        ready = select.select(rlist, [], [])
        msg = ready[0][0].read()
        if msg:
            do_email(
                args.mailserver,
                args.port,
                args.sender_user,
                args.sender_domain,
                password,
                args.recipients,
                msg,
                args.subject,
            )
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()
