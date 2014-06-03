"""This "hello world" service runs in the foreground (maybe via a cronjob,
or under another daemonizing script/infrastructure) and exits
"""

import getpass
import pwd

from zms.core.service import Service

class HelloWorldService(Service):
    def __init__(self):
        super(HelloWorldService, self).__init__('hello_world')

    def add_extra_arguments(self, parser):
        parser.add_argument('--name',
                            default=pwd.getpwnam(getpass.getuser()).pw_gecos,
                            )

    def parse_extra_arguments(self, args):
        self.name = args.name

    def run(self):
        self.logger.info("hello world, %s!", self.name)

if __name__ == '__main__':
    HelloWorldService().main()
