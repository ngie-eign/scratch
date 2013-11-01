#!/usr/bin/env python
"""
Entry point for the Web App for the project
"""

import frontend.settings as settings
from frontend.forms import app


if __name__ == '__main__':
    app.run(debug=2, host='0.0.0.0', port=80)

# Log on failures via email; based on:
# http://flask.pocoo.org/docs/errorhandling/
if not app.debug:
    from logging.handlers import SMTPHandler
    subject_line = 'Exception encountered on %s' % (settings.SITE_HOSTNAME)
    mail_handler = SMTPHandler(settings.SITE_MAIL_HOST,
                               settings.SITE_ADMINS[0],
                               settings.SITE_ADMINS,
                               subject_line,
                               credentials=(settings.SITE_MAIL_USER,
                                            settings.SITE_MAIL_PASSWORD),
                               secure=(),
                               )
    mail_handler.setLevel(settings.SITE_MAIL_LOG_LEVEL)
    app.logger.addHandler(mail_handler)
