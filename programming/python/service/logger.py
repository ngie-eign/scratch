"""
Logger module

.. moduleauthor:: Enji Cooper <yaneurabeya@gmail.com>
.. date: March 2014
"""

import logging
from logging.handlers import SysLogHandler


_LOGGER = None

FORMAT_VERBOSE = (
    "[%(name)s] [%(process)d] [%(threadName)s] %(module)s %(funcName)s %(levelname)s: "
    "%(message)s"
)


def init_logger(
    name=None,
    address="/dev/log",
    facility=SysLogHandler.LOG_LOCAL5,
    format=FORMAT_VERBOSE,
    level=logging.DEBUG,
):
    """Initialize the static logger instance

    Will reinitialize static logger instance if it is already set.

    :param name: the logger name passed on to logging.getLogger(..).
    :type name: string
    :param address: the address used when initializing the logger. This is
                    the same as address in SysLogHandler.__init__.
    :type address: string
    :param facility: the facility to use when logging. This is the same as
                      facility in SysLogHandler.__init__.
    :type facility: integer
    :param format: the format

    :returns: logging.SysLogHandler object
    """

    global _LOGGER

    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = SysLogHandler(address=address, facility=facility)
    handler.setFormatter(logging.Formatter(format))

    logger.addHandler(handler)

    _LOGGER = logger

    return _LOGGER


def get_logger():
    """Return static logger instance

    If the static logger instance has not been initialized, then
    a new one will be created and the level will be set to DEBUG.

    :returns: logging.SysLogHandler object
    """
    if _LOGGER is None:
        init_logger(name="Default_Logger", level=logging.DEBUG)
        _LOGGER.debug("Created default logger")
    return _LOGGER
