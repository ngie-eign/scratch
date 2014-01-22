#!/usr/bin/env python
"""
A dumb script that sits and punts emails across the wire in a while(1)
manner. Best used with FIFOs.

Sort of ripped from FreeNAS 8 (gui.common.system).

Example:

echo 'hello world!' | \
     python sendmail.py -d zonarsystems.com -m mail.zonarsystems.com -p 587 \
                        -s 'Hello world'

Garrett Cooper, October 2013
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import formatdate
import getpass
import os
import select
import smtplib
import socket
import sys
import time


def add_attachments(attachment_files):
    attachments = []
    for attachment_file in attachment_files:
        attachment = MIMEText(open(attachment_file, 'rb').read(),
                              _charset='utf-8')
        attachment.add_header('Content-Disposition', 'attachment',
                              filename=os.path.basename(attachment_file))
        attachments.append(attachment)
    return attachments


def do_email(mailserver, port, user, domain, password, recipients, message,
             subject, attachments=None):
    smtp_args = []
    if mailserver:
        smtp_args.append(mailserver)
        if port:
            smtp_args.append(port)

    user = user or getpass.getuser()
    domain = domain or socket.gethostname()

    server = smtplib.SMTP(*smtp_args, timeout=10)
    try:
        #server.set_debuglevel(1)
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()

        sender = '@'.join([user, domain]).encode('utf-8')

        if attachments:
            msg = MIMEMultipart()
            msg.preamble = message
            for attachment in attachments:
                msg.attach(attachment)
        else:
            msg = MIMEText(message, _charset='utf-8')
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Date'] = formatdate()
        msg['Subject'] = subject
        msg = msg.as_string()

        try:
            if password:
                server.login(user, password)
        except Exception as e:
            print('Error logging into server: %r' % (repr(e)))
            #time.sleep(10)
        res = server.sendmail(sender, recipients, msg)
        #if res:
        #    print('Error sending mail: %r' % (repr(res)))
        #else:
        #    print('Email sent!\n%s' % (msg, ))
    finally:
        server.quit()


def main():
    import optparse

    parser = optparse.OptionParser()
    parser.add_option('-d', default='.'.join(socket.getfqdn().split('.')[1:]),
                      dest='sender_domain',
                      help=('domain name to use for sender email '
                            '(default: %default)'),
                      )
    parser.add_option('-m', default='localhost',
                      dest='mailserver',
                      help='mailserver to use for relaying email',
                      )
    parser.add_option('-p', default=socket.getservbyname('smtp'),
                      dest='port',
                      type=int,
                      help='port to connect to SMTP on (default: %default)',
                      )
    parser.add_option('-s',
                      dest='subject',
                      help='subject line in email to send',
                      )
    parser.add_option('-u', default=os.getenv('USER'),
                      dest='sender_user',
                      help=('username to use when sending mail '
                            '(default: %default)'),
                      )

    opts, recipients = parser.parse_args()
    if not len(recipients):
        parser.exit('you must supply at least one recipient')

    password = os.getenv('PASSWORD') or getpass.getpass()
    password = password.strip().encode('utf-8')

    rlist = [sys.stdin]

    while True:
        ready = select.select(rlist, [], [])
        msg = ready[0][0].read()
        if msg:
            do_email(opts.mailserver, opts.port, opts.sender_user,
                     opts.sender_domain, password, recipients, msg,
                     opts.subject)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()

