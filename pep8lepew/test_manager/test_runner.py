#!/usr/bin/env python

import multiprocessing
import platform
import shlex
import subprocess


class TestRunner(object):
    """A test executer/runner
    """

    def execute(self, command):
        """Execute in a remote process

        :Parameters:
            command (str): a string that describes the command which will be
                           executed across the wire.

        :Returns:
            a tuple in the form: (stdout, stderr, returncode)
        """

        if not platform.platform().startswith('win'):
            command = shlex.split(command)

        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p.wait()

        return p.stdout, p.stderr, p.returncode


    def eval(self, code):
        """Evaluate in a remote process

        :Parameters:
            code (str): a string that describes the code that will be executed
                        across the wire.
        :Returns:
            is used defined based on the eval'ed code in ``code``.
        """

        eval(code)
