#!/usr/bin/env python

from . import (
    logger, make_logging_config, STDOUT_HANDLER, SYSLOG_LOCAL_HANDLER,
    SYSLOG_NETWORK_HANDLER
)


CUSTOM_LOGGER_NAME = "foo.bar.baz"
CUSTOM_LOGGER_CONFIG = make_logging_config(
    CUSTOM_LOGGER_NAME,
    {
        "level": "DEBUG",
        "handlers": [STDOUT_HANDLER, SYSLOG_LOCAL_HANDLER, SYSLOG_NETWORK_HANDLER],
    }
)


def get_custom_logger(name=CUSTOM_LOGGER_NAME):
    return logger(name, CUSTOM_LOGGER_CONFIG)


def func():
    logger(__name__).info("Calling Major Tom!")


def foo_bar_baz(*args, **kwargs):
    get_custom_logger().debug("args=%r, kwargs=%r", args, kwargs)


class Classy:
    def foo_bar_baz(self, *args, **kwargs):
        classy_custom_logger_name = "%s.with_class" % (CUSTOM_LOGGER_NAME)
        custom_logger = get_custom_logger(name=classy_custom_logger_name)
        custom_logger.critical("args=%r, kwargs=%r", args, kwargs)


func()
foo_bar_baz("a", 1, b=2, c="str")
Classy().foo_bar_baz("a", 1, b=2, c="str")
