#!/usr/bin/env python

import telnetlib
import time


class SnoopyTelnet(telnetlib.Telnet):
    # NOTE: telnetlib.Telnet is not a new-style class, so super will not work
    # here.

    def __init__(self, logfile, logfile_mode='wb', *args, **kwargs):
        self._logfile = None
        self.logfile = logfile
        self.logfile_mode = logfile_mode

        telnetlib.Telnet.__init__(self, *args, **kwargs)

    def open(self, *args, **kwargs):
        telnetlib.Telnet.open(self, *args, **kwargs)

        self._logfile = open(self.logfile, self.logfile_mode)
        self._logfile.write('Logging started on %s %s\n'
                            % (time.asctime(time.gmtime()), time.tzname[-1]))

    def close(self):
        if self._logfile is not None and not self._logfile.closed:
            self._logfile.write('\nLogging ended on %s %s\n'
                                % (time.asctime(time.gmtime()), time.tzname[-1]))
            self._logfile.flush()
            self._logfile.close()
        telnetlib.Telnet.close(self)

    def fill_rawq(self):
        telnetlib.Telnet.fill_rawq(self)
        try:
            self._logfile.write(self.rawq)
        except IOError:
            pass

    def write(self, buf):
        try:
            self._logfile.write(buf)
        except IOError:
            pass
        telnetlib.Telnet.write(self, buf)


if __name__ == '__main__':
    tn = SnoopyTelnet(host='www.goodellgroup.com', port=80, logfile='webpage.log')
    tn.write('GET /tutorial/chapter4.html HTTP/1.1\n\n')
    tn.read_until('</html>')
    tn = SnoopyTelnet(host='www.google.com', port=80, logfile='google.log')
    tn.write('GET /index.html HTTP/1.1\n\n')
    tn.read_until('</html>')
