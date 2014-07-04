#!/usr/bin/env python

import fcntl
import multiprocessing
import os
import select
import telnetlib


def locked_write(logfile_fd, buf, logfile_lock):
    #print '[pid=%d] Writing message to logfile: %s' % (os.getpid(), buf)
    logfile_lock.acquire()
    try:
        logfile_fd.write(buf)
        logfile_fd.flush()
    finally:
        logfile_lock.release()


def log_from_socket(sock_fd, logfile_fd, logfile_lock):
    with os.fdopen(sock_fd) as sock:
        #fcntl.fcntl(sock, fcntl.F_SETFL, os.O_NONBLOCK)
        while True:
            try:
                print '[pid=%d] I am the child' % (os.getpid(), )

                msg = ''
                while True:
                    read_list, _, _ = select.select([sock], [], [], 2)
                    if not read_list:
                        break
                    print '[pid=%d] The child got a message' % (os.getpid(), )
                    buf = read_list[0].read(10)
                    if not buf:
                        break
                    msg += buf
                if msg:
                    locked_write(logfile_fd, msg, logfile_lock)
            except IOError:
                break


class SnoopyTelnet(telnetlib.Telnet):
    # NOTE: telnetlib.Telnet is not a new-style class, so super will not work
    # here.

    def __init__(self, logfile, *args, **kwargs):
        self.logfile = logfile
        self._logfile_fd = None
        self._logfile_lock = multiprocessing.Lock()
        self._logfile_reader = None

        telnetlib.Telnet.__init__(self, *args, **kwargs)

    def open(self, *args, **kwargs):
        telnetlib.Telnet.open(self, *args, **kwargs)

        p_args = []
        self._logfile_fd = open(self.logfile, 'w')
        try:
            p_args = (os.dup(self.fileno()),
                      self._logfile_fd,
                      self._logfile_lock,
                      )
            self._logfile_reader = \
                multiprocessing.Process(target=log_from_socket, args=p_args)
            self._logfile_reader.start()
        except:
            self._logfile_fd.close()
            if p_args:
                p_args[0].close()
            raise

    def close(self):
        telnetlib.Telnet.close(self)

        if self._logfile_fd:
            self._logfile_fd.close()
            self._logfile_fd = None
        if self._logfile_reader.is_alive():
            #self._logfile_reader.terminate()
            self._logfile_reader.join()

    def write(self, buf):
        print '[pid=%d] Parent is writing a message: %s' % (os.getpid(), buf)
        telnetlib.Telnet.write(self, buf)
        try:
            locked_write(self._logfile_fd, buf, self._logfile_lock)
            self._logfile_fd.write(buf)
        except IOError:
            pass


print '[pid=%d] I am the parent' % (os.getpid(), )
tn = SnoopyTelnet(host='www.google.com', port=80, logfile='google.log')
tn.write('GET /index.html HTTP/1.1\n\n')
tn.read_until('.*')
tn.close()
