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
import hashlib
import optparse
import os
import signal
import socket
import sys


EXIT = False


def client_verify_handler(sock, read_length):
    """Client socket hash verification handler"""

    buf = ''
    while len(buf) != read_length:
        rbuf = sock.recv(min(read_length, read_length-len(buf)))
        if not rbuf:
            break
        buf += rbuf

    buf = hashlib.sha256(buf).hexdigest()
    buf2 = sock.recv(1024)
    if buf == buf2:
        sys.stdout.write('Hashes matched\n')
    else:
        sys.stderr.write('Hashes did not match: `%s` != `%s`\n' % (buf, buf2))
        os._exit(1)


def client_noverify_handler(sock, read_length):
    """Client socket no-hash verification handler"""

    while True:
        if not sock.recv(8192):
            break


def conn_handler_bounded(sock, read_fd, read_length):
    """Connection handler when read_length > 0"""

    buf = ''
    while True:
        rbuf = read_fd.read(min(8192, read_length-len(buf)))
        sock.sendall(rbuf)
        buf += rbuf
        if read_length == len(buf):
            break

    buf2 = hashlib.sha256(buf).hexdigest()
    sock.sendall(buf2)


def conn_handler_unbounded(sock, read_fd, read_length):
    """Connection handler when read_length < 0"""

    while True:
        try:
            sock.send(read_fd.read(65536))
        except socket.error:
            return


def do_client(sock, host, port, input_file, offset, read_length):
    """Do client stuff"""

    sock.connect((host, port))
    sock.send('%s %d %d' % (input_file, offset, read_length))
    rbuf = sock.recv(3)
    if rbuf != 'OK':
        sys.exit('Invalid message received: %s' % (rbuf))
    sock.send('GO')
    if 0 < read_length:
        client_verify_handler(sock, read_length)
    else:
        client_noverify_handler(sock, read_length)


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

            try:
                exit_code = 2
                buf = inc_sock.recv(1024)
                input_file, offset, req_length = buf.split()
                offset = long(offset)
                req_length = long(req_length)
                if offset < 0:
                    inc_sock.sendall('BADREQUEST: offset negative')
                elif read_length != -1 and read_length < req_length:
                    inc_sock.sendall('BADREQUEST: read length too long '
                                     '(%d < %d)' % (read_length, req_length))
                else:
                    exit_code = 1
                    try:
                        with open(input_file, 'rb') as fd:
                            if 0 < offset:
                                fd.seek(offset, os.SEEK_SET)
                            inc_sock.sendall('OK')
                            inc_sock.recv(2)
                            if 0 < req_length:
                                conn_handler_bounded(inc_sock, fd,
                                                     req_length)
                                exit_code = 0
                            else:
                                conn_handler_unbounded(inc_sock, fd,
                                                       req_length)

                    except socket.error:
                        pass
                    #except IOError:
                    #    exit_code = 0
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


    def port_cb(option, opt_s, val, parser):
        """--port handler"""

        port_min = 1
        port_max = 65535
        if int(val) not in range(1, port_max+1):
            raise optparse.OptionValueError('Value passed to %s must be an '
                                            'integer between %d and %d'
                                            % (opt_s, port_min, port_max))
        parser.values.port = int(val)


    usage = ('usage: %prog [options] -s inputfile\n'
             '       %prog [options]')

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-A', '--address-family',
                      action='callback',
                      callback=address_family_cb,
                      default=socket.AF_UNSPEC,
                      dest='address_family',
                      help=('Address family to use when connecting/listening'
                            '(%s)' % (af_supported_values_s)),
                      type='int',
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
