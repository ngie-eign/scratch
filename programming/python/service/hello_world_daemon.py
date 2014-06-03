"""This "hello world" service runs in the foreground (maybe via a cronjob,
or under another daemonizing script/infrastructure) and exits
"""

from zms.core.service import Daemon

class HelloWorldDaemon(Daemon):
    def __init__(self):
        super(HelloWorldDaemon, self).__init__('hello_world')

    def run(self):
        self.logger.info("hello world!")

if __name__ == '__main__':
    HelloWorldDaemon().main()
