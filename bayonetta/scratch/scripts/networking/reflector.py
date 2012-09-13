#!/usr/bin/env python
"""
Simple reflection module with verification support

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

import atexit
import errno
import optparse
import os
import signal
import socket
import sys


EXIT = False

TWOMEG = 2 * 1024 * 1024

def client_handler(sock, req_length):
    """Client handler"""

    read_length = 0
    while read_length < req_length:
        buf = sock.recv(min(TWOMEG, req_length-read_length))
        if not buf:
            sys.stderr.write('EOF starting with chunk at: %d\n' % (read_length))
            break
        sent = 0
        while sent < len(buf):
            sent_l = sock.send(buf[sent:])
            if not sent_l:
                break
            sent += sent_l
        read_length += sent
        if sent != len(buf):
            break

    if read_length == req_length:
        sys.stdout.write('Requested data transmitted successfully\n')
        exit_code = 0
    else:
        sys.stderr.write('Requested data not retransmitted completely (%d != '
                         '%d)\n' % (read_length, req_length))
        exit_code = 1
    os._exit(exit_code)


def request_handler(sock, read_fd, req_length):
    """Request handler"""

    rl = (sock, )
    read_length = 0
    while read_length < req_length:
        buf = read_fd.read(min(TWOMEG, req_length-read_length))
        sent = 0
        while sent < len(buf):
            sent += sock.send(buf[sent:])
        rbuf = ''
        rbuf_l = ''
        while len(rbuf) < len(buf):
            rbuf_l = sock.recv(len(buf))
            if not rbuf_l:
                break
            rbuf += rbuf_l
        if not rbuf:
            sys.stderr.write('EOF starting with chunk at: %d\n' % (read_length))
            break
        if buf != rbuf:
            sys.stderr.write('Mismatch starting with chunk at: %d\n' % (read_length))
            break
        read_length += sent

    if read_length == req_length:
        sys.stdout.write('Data transmitted successfully\n')
        exit_code = 0
    else:
        sys.stderr.write('Requested data not retransmitted completely (%d != '
                         '%d)\n' % (read_length, req_length))
        exit_code = 1
    return exit_code


def do_client(sock, host, port, input_file, offset, read_length):
    """Do client stuff"""

    sock.connect((host, port))
    sock.send('%s %d %d' % (input_file, offset, read_length))
    rbuf = sock.recv(1024)
    if rbuf != 'OK':
        sys.exit('Invalid message received: %s' % (rbuf))
    sock.send('GO')
    client_handler(sock, read_length)


def server_exit():
    """Common function for handling graceful server exits"""

    global EXIT
    EXIT = True


def do_server(sock, host, port, read_length):
    """Do server stuff"""

    def server_sighandler(signo, stack):
        """Signal handler for the server"""

        server_exit()


    atexit.register(server_exit)
    signal.signal(signal.SIGINT, server_sighandler)
    signal.signal(signal.SIGTERM, server_sighandler)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN) 

    sock.bind((host, port))
    sock.listen(100)

    while not EXIT:

        try:
            inc_sock, __ = sock.accept()
        except socket.error, err:
            if err.errno == errno.EINTR:
                break

        child = os.fork()
        if child:
            inc_sock.close()
        else:
            #inc_sock.setsockopt(socket.IPPROTO_TCP, socket.SO_RCVTIMEO, 30)
            #inc_sock.setsockopt(socket.IPPROTO_TCP, socket.SO_SNDTIMEO, 30)
            try:
                exit_code = 2
                buf = inc_sock.recv(1024)
                input_file, offset, req_length = buf.split()
                offset = long(offset)
                req_length = long(req_length)
                if offset < 0:
                    inc_sock.sendall('BADREQUEST: offset negative')
                elif req_length <= 0:
                    inc_sock.sendall('BADREQUEST: request length <= 0')
                elif (read_length < req_length or
                      (os.path.isfile(input_file) and
                       os.stat(input_file).st_size < req_length)):
                    inc_sock.sendall('BADREQUEST: request length too long '
                                     '(%d < %d)' % (read_length, req_length))
                else:
                    exit_code = 1
                    with open(input_file, 'rb') as fd:
                        fd.seek(offset, os.SEEK_SET)
                        inc_sock.sendall('OK')
                        inc_sock.recv(2)
                        exit_code = request_handler(inc_sock, fd, req_length)
            finally:
                inc_sock.close()

            os._exit(exit_code)


def main(argv):
    """Main"""

    af_supported_values_mapping = {
        '4': socket.AF_INET,
        '6': socket.AF_INET6,
        '' : socket.AF_UNSPEC,
    }
    af_supported_values_s = '4, 6, or ""'

    def address_family_cb(option, opt_s, val, parser):
        """--address-family handler"""

        af = af_supported_values_mapping.get(val)
        if af is None:
            raise optparse.OptionValueError('%s only supports %s'
                                            % (opt_s, af_supported_values_s))
        parser.values.address_family = af


    def length_cb(option, opt_s, val, parser):
        """--length handler"""

        if val <= 0:
            raise optparse.OptionValueError('Value passed to %s must be '
                                            'greater than 0' % (opt_s))
        parser.values.length = val


    def port_cb(option, opt_s, val, parser):
        """--port handler"""

        port_min = 1
        port_max = 65535
        if val not in range(1, port_max+1):
            raise optparse.OptionValueError('Value passed to %s must be an '
                                            'integer between %d and %d'
                                            % (opt_s, port_min, port_max))
        parser.values.port = val


    usage = ('usage: %prog [options] inputfile\n'
             '       %prog [options] -s')

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-A', '--address-family',
                      action='callback',
                      callback=address_family_cb,
                      default=socket.AF_UNSPEC,
                      dest='address_family',
                      help=('Address family to use when connecting/listening'
                            '(%s)' % (af_supported_values_s)),
                      type='str',
                      )
    parser.add_option('-H', '--host',
                      default='',
                      dest='host',
                      help='Host to connect/bind to',
                      type='str',
                      )
    parser.add_option('-l', '--length',
                      action='callback',
                      callback=length_cb,
                      default=(256 * 1024),
                      dest='read_length',
                      help='Length of data to read back across the wire',
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
                      type='int',
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
                      help='Send buffer size for sockets',
                      type='int',
                      )

    opts, args = parser.parse_args(args=argv)
    if opts.server_mode:
        if args:
            parser.error('Spurious arguments: %s' % (' '.join(args)))
    else:
        if not args:
            parser.error('You must provide an input file when running as a '
                         'client')
        input_file = args[0]

    if opts.host and opts.address_family != socket.AF_UNSPEC:
        addr = socket.inet_pton(opts.address_family, opts.host)
        sock = socket.socket(opts.address_family)
    elif not opts.host:
        addr = ''
        sock = socket.socket()
    else:
        addr = opts.host
        if opts.address_family == socket.AF_UNSPEC:
            sock = socket.socket()
        else:
            sock = socket.socket(opts.address_family)

    if 0 < opts.rcvbuf_size:
        sock.setsockopt(socket.IPPROTO_IP, socket.SO_RCVBUF, opts.rcvbuf_size)
    if 0 < opts.sndbuf_size:
        sock.setsockopt(socket.IPPROTO_IP, socket.SO_SNDBUF, opts.sndbuf_size)

    try:
        if opts.server_mode:
            do_server(sock, addr, opts.port, opts.read_length)
        else:
            do_client(sock, addr, opts.port, input_file, opts.offset,
                      opts.read_length)
    finally:
        sock.close()


if __name__ == '__main__':
    main(sys.argv[1:])
