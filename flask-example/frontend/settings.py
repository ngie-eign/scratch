import getpass
import logging
import os
import socket
import sys


def em_obfuscate(username, domain):
    # Screw you spambots
    return '@'.join([username, domain])


# Email logging settings.
SITE_ADMINS = map(lambda x: em_obfuscate(x[0], x[1]), [
                   ('garrett.cooper', 'zonarsystems.com'),
                  ])
SITE_HOSTNAME = socket.getfqdn()
SITE_MAIL_LOG_LEVEL = logging.ERROR
SITE_MAIL_HOST = os.getenv('SITE_MAIL_HOST') or 'localhost'
if ':' in SITE_MAIL_HOST:
    SITE_MAIL_HOST = SITE_MAIL_HOST.split(':')
    SITE_MAIL_HOST[-1] = int(SITE_MAIL_HOST[-1])
    SITE_MAIL_HOST = tuple(SITE_MAIL_HOST)
SITE_MAIL_USER = os.getenv('SITE_MAIL_USER') or getpass.getuser()
SITE_MAIL_PASSWORD = os.getenv('SITE_MAIL_PASSWORD') or \
    (sys.stdin.isatty() and getpass.getpass())
