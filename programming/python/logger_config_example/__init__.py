#!/usr/bin/env python

import copy
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache
import logging
import logging.config
import logging.handlers
import sys  # noqa: F401


_CONFIG_TEMPLATE = {
    "version": 1,
    "disable_existing_loggers": False,
}


def make_logging_config(name=None, logger_definition=None):
    logging_config = copy.deepcopy(_CONFIG_TEMPLATE)
    if name is not None:
        logging_config["loggers"] = {
            name: logger_definition
        }
    return logging_config


_PATH_LOG = "/dev/log"
DEFAULT_FORMATTER = "formatter"
DEFAULT_LOGGER = "default"
STDOUT_HANDLER = "stdout"
SYSLOG_LOCAL_HANDLER = "syslog_local"
SYSLOG_NETWORK_HANDLER = "syslog_network"

_DEFAULT_LOGGING_CONFIG = make_logging_config()
_DEFAULT_LOGGING_CONFIG.update({
    "formatters": {
        DEFAULT_FORMATTER: {
            "class": "logging.Formatter",
            "format": "%(asctime)-15s %(name)s[%(process)d]: %(levelname)s %(message)s",
            "datefmt": ""
        }
    },
    "handlers": {
        STDOUT_HANDLER: {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": DEFAULT_FORMATTER,
            "stream": "ext://sys.stdout"
        },
        SYSLOG_LOCAL_HANDLER: {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "formatter": DEFAULT_FORMATTER,
            "address": _PATH_LOG,
            "facility": "daemon"
        },
        SYSLOG_NETWORK_HANDLER: {
            "class": "logging.handlers.SysLogHandler",
            "level": "DEBUG",
            "formatter": DEFAULT_FORMATTER,
            # "localhost" is implied for `address`.
            "facility": "daemon"
        }
    },
    # "loggers"
    "root": {
        "handlers": ["stdout"],
        "level": "DEBUG",
        "propagate": True,
    }
})
print(_DEFAULT_LOGGING_CONFIG)


#@lru_cache(maxsize=128)
def _init_loggers_from_config(logging_config):
    logging.config.dictConfig(logging_config)


def logger(name, logging_config=None):
    _init_loggers_from_config(_DEFAULT_LOGGING_CONFIG)
    if logging_config is not None:
        _init_loggers_from_config(logging_config.items())
    return logging.getLogger(name)
