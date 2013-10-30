#!/usr/bin/env python

from email.mime.text import MIMEText
from email.Utils import formatdate
import getpass
import smtplib
import sys
import time

mailserver = 'mail.zonarsystems.com'
password = getpass.getpass().strip().encode('utf-8')
port = 587

server = smtplib.SMTP(
    mailserver,
    port,
    timeout=10,
)
server.starttls()

def em_obfuscate(username, domain):
    # Screw you spambots
    return '@'.join([username, domain]).encode('utf-8')

sender = em_obfuscate('garrett.cooper', 'zonarsystems.com')
recipients = \
    map(lambda x: em_obfuscate(x[0], x[1]), [('yaneurabeya', 'gmail.com')])

while True:

    msg = MIMEText(sys.stdin.read())
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate()
    print msg

    try:
        server.login(
            sender,
            password,
        )
    except Exception as e:
        print('Error logging into server: %s' % (str(e)))
        time.sleep(10)
        continue
    try:
        server.sendmail(sender, recipients, msg, _charset='utf-8')
    finally:
        server.quit()
