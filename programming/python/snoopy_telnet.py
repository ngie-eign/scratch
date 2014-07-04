#!/usr/bin/env python

import telnetlib


class SnoopyTelnet(telnetlib.Telnet):
    # NOTE: telnetlib.Telnet is not a new-style class, so super will not work
    # here.

    def __init__(self, logfile, *args, **kwargs):
        self.logfile = logfile
        self._logfile = None

        telnetlib.Telnet.__init__(self, *args, **kwargs)

    def open(self, *args, **kwargs):
        telnetlib.Telnet.open(self, *args, **kwargs)

        self._logfile = open(self.logfile, 'wb')

    def close(self):
        if self._logfile is not None:
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
