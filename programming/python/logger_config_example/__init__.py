#!/usr/bin/env python

import logging
import logging.config
import logging.handlers
import sys


DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "formatter": {
            "class": "logging.Formatter",
            "format": "%(asctime)-15s %(name)s[%(process)d]: %(levelname)s %(message)s",
            "datefmt": ""
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "formatter",
            "stream": "ext://sys.stdout"
        },
        "syslog_file": {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "formatter": "formatter",
            "address": "/dev/log",
            "facility": "daemon"
        },
        "syslog_network": {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "formatter": "formatter",
            # "localhost" is implied for `address`.
            "facility": "daemon"
        }
    },
    "loggers": {
        "foo.bar.baz": {
            "level": "DEBUG",
            "handlers": ["stdout", "syslog_file"],
        }
    },
    "root": {
        "handlers": ["stdout"],
        "level": "DEBUG",
        "propagate": True,
    }
}


def logger(name):
    logging.config.dictConfig(DEFAULT_CONFIG)
    return logging.getLogger(name)
