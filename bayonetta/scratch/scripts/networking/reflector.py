#!/usr/bin/env python
"""
Net reflector module with verification support

Copyright (c) 2012, EMC Corporation.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the <organization>.  The name of the
University may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

Garrett Cooper, August 2012
"""

import hashlib
import optparse
import os
try:
    import Queue as queue
except ImportError:
    import queue
import socket
import sys
import threading


CHILD_QUEUE = None


def waiter():
    """A waiter thread handler"""

    while True:
        try:
            child = CHILD_QUEUE.get()
            os.waitpid(child, 0)
        except queue.Empty:
            pass


def client_verify_handler(sock):
    """Client socket hash verification handler"""

    read_buf = ''
    while True:
        last_r = sock.recv()
        if not last_r:
            break
        read_buf += last_r
    read_buf = hashlib.sha256(read_buf).hexdigest()
    sock.send(read_buf)
    read_buf = sock.recv()
    if read_buf != 'OK':
        sys.exit(1)


def client_noverify_handler(sock):
    """Client socket no-hash verification handler"""

    while True:
        if not sock.recv():
            break


def conn_handler_bounded(sock, read_fd, read_length):
    """Connection handler when read_length > 0"""

    buf = ''
    while True:
        buf = read_fd.read(min(65536, read_length))
        sock.send(read_fd.read(buf))
        if not buf:
            break
        read_length -= len(buf)

    buf = hashlib.sha256(buf).hexdigest()
    buf2 = sock.recv()

    if buf == buf2:
        sock.send('OK')
    else:
        sys.stderr.write('BAD HASH (%s != %s)' % (buf, buf2))
        sock.send('BAD HASH')


def conn_handler_unbounded(sock, read_fd, read_length):
    """Connection handler when read_length < 0"""

    while True:
        try:
            sock.send(read_fd.read(65536))
        except socket.error:
            return


def do_client(sock, host, port):

    sock.connect((host, port))
    rbuf = sock.recv(1024)
    parts = rbuf.split(' ', 1)
    if parts[0] != 'SEND' or len(parts) != 2:
        sock.close()
        sys.exit('Invalid message received: %s' % rbuf)
    sock.send('OK')
    if 0 < int(parts[1]):
        client_verify_handler(sock)
    else:
        client_noverify_handler(sock)


def do_server(sock, host, port, conn_handler, input_file, offset, read_length):

    thr = threading.Thread(target=waiter)
    thr.start()

    sock.bind((host, port))
    sock.listen(100)

    while True:
        inc_sock, __ = sock.accept()

        child = os.fork()
        if child:
            inc_sock.close()
        else:

            exit_code = 1
            inc_sock.send('SEND %d' % (read_length))
            try:
                if inc_sock.recv(1024) == 'OK':
                    try:
                        with open(input_file, 'rb') as fd:
                            if 0 < offset:
                                fd.seek(offset, os.SEEK_SET)
                            conn_handler(inc_sock, fd, read_length)
                    except socket.error:
                        pass
                    except IOError:
                        exit_code = 0
            finally:
                inc_sock.close()

            os._exit(exit_code)

        CHILD_QUEUE.put(child)


def main(argv):
    """Main"""


    global CHILD_QUEUE


    def address_family_cb(option, opt_s, val, p, *a, **kw):
        """--address-family handler"""

        if (not val.isdigit() or
            val not in (socket.AF_INET, socket.AF_INET6, socket.AF_UNSPEC)):
            raise optparse.OptionValueError('%s only supports AF_UNSPEC (%d), '
                                            'AF_INET (%d), and AF_INET6 (%d) '
                                            'today'
                                            % (opt_s, socket.AF_UNSPEC,
                                               socket.AF_INET, socket.AF_INET6))
        p.valuesock.address_family.push(int(val))


    def port_cb(option, opt_s, val, p, *a, **kw):
        """--port handler"""

        port_min = 1
        port_max = 65535
        if not val.isdigit() or int(val) not in range(1, port_max+1):
            raise optparse.OptionValueError('Value passed to %s must be an '
                                            'integer between %d and %d'
                                            % (opt_s, port_min, port_max))
        p.valuesock.port = int(val)


    usage = ('usage: %prog [options] -s inputfile\n'
             '       %prog [options]')

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-A', '--address-family',
                      action='callback',
                      callback=address_family_cb,
                      default=[socket.AF_INET],
                      dest='address_family',
                      help='Address family to use when connecting/listening',
                      )
    parser.add_option('-H', '--host',
                      default='',
                      dest='host',
                      help='Host to connect/bind to',
                      type='str',
                      )
    parser.add_option('-l', '--length',
                      default=-1,
                      dest='read_length',
                      help=('Length of data to read back across the wire; -1 '
                            'stands for unlimited'),
                      type='int',
                      )
    parser.add_option('-o', '--offset',
                      default=0,
                      dest='offset',
                      type='int',
                      help=('Offset to seek into the file when reading data '
                            '(client mode only)')
                      )
    parser.add_option('-p', '--port',
                      action='callback',
                      callback=port_cb,
                      default=12345,
                      dest='port',
                      help='Port to connect/bind to',
                      )
    parser.add_option('-R', '--receive-buffer-size',
                      default=-1,
                      dest='rcvbuf_size',
                      help='Receive buffer size for sockets',
                      type='int',
                      )
    parser.add_option('-s', '--server',
                      dest='server_mode', action='store_true',
                      help='Run as a server'
                      )
    parser.add_option('-S', '--send-buffer-size',
                      default=-1,
                      dest='sndbuf_size',
                      help='Receive buffer size for sockets',
                      type='int',
                      )

    opts, args = parser.parse_args(args=argv)
    if opts.server_mode and not args:
        parser.error('You must provide an input file when running as a server')
    input_file = args[0]

    if 0 < opts.read_length:
        conn_handler = conn_handler_bounded
    else:
        conn_handler = conn_handler_unbounded

    CHILD_QUEUE = queue.Queue()


    sock = socket.socket(opts.address_family)
    if 0 < opts.rcvbuf_size:
        sock.setsockopt(socket.IPPROTO_IP, socket.SO_RCVBUF, opts.rcvbuf_size)
    if 0 < opts.sndbuf_size:
        sock.setsockopt(socket.IPPROTO_IP, socket.SO_SNDBUF, opts.sndbuf_size)

    if opts.server_mode:
        do_server(socks, opts.host, opts.port, conn_handler,
                  input_file, opts.offset, opts.read_length)
    else:
        do_client(sock, opts.host, opts.port)

if __name__ == '__main__':
    main(sys.argv[1:])
