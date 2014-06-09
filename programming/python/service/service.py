"""
Module for defining daemons and services.

.. moduleauthor:: Garrett Cooper <garrett.cooper {at} {DONT-SPAM-ME} {dot} zonarsystems.com>
.. date: March 2014
"""

from argparse import ArgumentParser
from ConfigParser import RawConfigParser
#import grp
import os
#import pwd
import sys

import daemon
# pylint: disable=F0401
import lockfile.pidlockfile as pidlockfile

from .logger import (
     get_logger,
     init_logger,
)

VAR_RUN_PATH = '/var/run'


class Service(object):
    """An abstract class for defining services

    The concrete class must implement:
    - run(..)

    The concrete class may implement:
    - add_extra_arguments(..)
    - parse_extra_arguments(..)

    The object should be instantiated and the object can and should
    immediately call main(..):

    >>> ServiceClass('my_service').main()
    """


    def __init__(self, service_name):
        """
        :param service_name: a unique, easy to search for service name, e.g.
                             `my_service`.
        :type service_name: string
        """
        self.config = None
        self.logger = None
        self.pidfile = None
        self.service_name = service_name


    def parse_args_pre(self, parser):
        """Operations to perform on `parser` before parsing the arguments.

        This should only be overridden by other abstract classes.

        :param parser: argument parser
        :type parser: argparse.ArgumentParser
        """

        self.add_extra_arguments(parser)


    def parse_args_post(self, args):
        """Operations to perform on `args` after parsing the arguments.

        This should only be overridden by other abstract classes.

        :param args: arguments
        :type args: argparse.Namespace
        """

        self.parse_extra_arguments(args)


    def run(self):
        """Abstract method that defines the core behavior of the service.
        """
        raise NotImplementedError


    def setup(self, argv=None, usage=None):
        """Performs of the "setup" operations, i.e. parsing arguments, reading
        the configuration file, setting up logging, etc.

        :param argv: arguments passed from the command-line. If not specified,
                     i.e. None, it will default to sys.argv.
        :type argv: list of strings
        """

        parser = ArgumentParser(usage=usage)

        parser.add_argument('--conf', '-C', dest='config_file',
                            help='configuration file',
                            #default=PATH,
                            )

        self.parse_args_pre(parser)
        args = parser.parse_args(argv)
        self.parse_args_post(args)

        init_logger()
        self.logger = get_logger()

        self.config = RawConfigParser()
        if not self.config.read(args.config_file):
            sys.exit('Could not read config file: %s' % (args.config_file, ))


    def main(self, argv=None, usage=None):
        """main wrapper function"""

        self.setup(argv=argv, usage=usage)

        self.logger.info('Starting service')
        try:
            self.run()
        except (KeyboardInterrupt, SystemExit):
            pass
        self.logger.info('Stopping service')


    def add_extra_arguments(self, parser):
        """Add additional service arguments"""


    def parse_extra_arguments(self, args):
        """Parse additional service arguments"""


class Daemon(Service):
    """An abstract class for defining daemons that builds upon the Service
    class
    """

    def parse_args_pre(self, parser):
        """Add additional argument parsing to `parser` for Daemons.

        This includes:
        -- --no-daemon
        -- --pidfile
        -- --runas-group (currently unused)
        -- --runas-user (currently unused)

        See also: Service.parse_args_pre(..)
        """
        default_pidfile_path = \
            os.path.join(VAR_RUN_PATH, '%s.pid' % (self.service_name, ))

        parser.add_argument('--no-daemon', '-D', dest='daemonize',
                            action='store_false',
                            default=True,
                            help='do not daemonize',
                            )
        parser.add_argument('--pidfile', '-p', dest='pidfile',
                            help='PID file',
                            default=default_pidfile_path,
                            )
        parser.add_argument('--runas-group',
                            help='Group to run as',
                            default='zuser',
                            )
        parser.add_argument('--runas-user',
                            help='User to run as',
                            default='zuser',
                            )
        super(Daemon, self).parse_args_pre(parser)


    def parse_args_post(self, args):
        """Handle additional argument parsing via `args` for Daemons.

        See also: Service.parse_args_post(..)
        """

        self.daemonize = args.daemonize
        self.pidfile = args.pidfile
        # XXX: doesn't work; always fails with EPERM because python exe doesn't
        # have setuid/setgid perms
        self.runas_group = None #grp.getgrnam(args.runas_group).gr_gid
        self.runas_user = None #pwd.getpwnam(args.runas_user).pw_uid

        super(Daemon, self).parse_args_post(args)


    def main(self, argv=None, usage=None):
        """Handle either running in the foreground or creating a
        pidfile/daemonizing

        See also: Service.main(..)
        """

        self.setup(argv=argv, usage=None)


        if not self.daemonize:
            self.logger.info('Starting daemon in foreground')
            try:
                self.run()
            except (KeyboardInterrupt, SystemExit):
                pass
            self.logger.info('Stopping daemon in foreground')
            return

        self.logger.info('Starting daemon')
        try:
            pidlock_obj = pidlockfile.PIDLockFile(self.pidfile, timeout=0)
        except:
            self.logger.exception('Failed to create the pidfile object')
            raise

        try:
            with daemon.DaemonContext(pidfile=pidlock_obj,
                                      gid=self.runas_group,
                                      uid=self.runas_user):
                self.logger.info('Entering run')
                self.run()
        except (KeyboardInterrupt, SystemExit):
            pass
        except:
            self.logger.exception('Failed to daemonize')
            raise

        self.logger.info('Stopping daemon')
