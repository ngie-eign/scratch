#!/usr/bin/env python
"""
A dumb script that sits and punts emails across the wire in a while(1)
manner. Best used with FIFOs.

Sort of ripped from FreeNAS 8 (gui.common.system).

Garrett Cooper, October 2013
"""

from email.mime.text import MIMEText
from email.Utils import formatdate
import getpass
import os
import smtplib
import sys
import time

def do_email(mailserver, port, user, domain, password, recipients, message):
    server = smtplib.SMTP(mailserver, port, timeout=10)
    try:
        #server.set_debuglevel(1)
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()

        sender = '@'.join([user, domain]).encode('utf-8')

        msg = MIMEText(message, _charset='utf-8')
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg['Date'] = formatdate()
        msg['Subject'] = 'Hello!'
        msg = msg.as_string()

        try:
            server.login(user, password)
        except Exception as e:
            print('Error logging into server: %r' % (repr(e)))
            #time.sleep(10)
        res = server.sendmail(sender, recipients, msg)
        if res:
            print('Error sending mail: %r' % (repr(res)))
        else:
            print('Email sent!\n%s' % (msg, ))
    finally:
        server.quit()

def main():
    if len(sys.argv) < 2:
        sys.exit('usage: %s email...' % (os.path.basename(sys.argv[0]), ))

    user = os.environ.get('USER', getpass.getuser())
    domain = os.environ.get('DOMAIN', 'zonarsystems.com')

    mailserver = 'mail.zonarsystems.com'
    password = os.environ.get('PASSWORD',
                              getpass.getpass()).strip().encode('utf-8')
    port = os.environ.get('PORT', 587)
    recipients = sys.argv[1:]

    while True:
        msg = sys.stdin.read()
        if msg:
            do_email(mailserver, port, user, domain, password, recipients, msg)

if __name__ == '__main__':
    main()
