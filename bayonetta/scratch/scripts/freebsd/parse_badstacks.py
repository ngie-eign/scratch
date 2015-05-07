#!/usr/bin/env python
"""
 Copyright (c) 2015 EMC Corp.
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 SUCH DAMAGE.

Dump out debug.witness.badstacks in either plaintext or JSON format.
"""

import json
import optparse
import re
import subprocess
import sys

BAD_STACKS_SYSCTL_OID = 'debug.witness.badstacks'
BAD_STACK_START = r'Lock order reversal between "([^"]+)"\(\w+\) and "([^"]+)"\(\w+\)!\n+'


def main(argv=None):
    parser = optparse.OptionParser()
    parser.add_option('--json-format', default=False, help='dump in JSON format',
                      action='store_true')
    parser.add_option('--json-pretty-print', default=False, help='pretty print JSON',
                      action='store_true')
    parser.add_option('--omit-stacks', default=False, help='omit stack backtraces',
                      action='store_true')
    opts, args = parser.parse_args(argv)
    if args:
        parser.usage('Superfluous options: %s' % (args, ))

    pipe = subprocess.Popen(['sysctl', '-n', BAD_STACKS_SYSCTL_OID],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = pipe.communicate()
    if pipe.returncode != 0:
        sys.stderr.write('Could not read %s: %s\n' % (BAD_STACKS_SYSCTL_OID, stdout, ))
        sys.exit(0)

    parse_and_print_bad_stacks(stdout,
                               json_format=opts.json_format,
                               json_pretty_print=opts.json_pretty_print,
                               omit_stacks=opts.omit_stacks)


def parse_and_print_bad_stacks(output,
                               json_format=False,
                               json_pretty_print=False,
                               omit_stacks=False,
                              ):

    # This effectively parses all badstacks groupings. If "!" no longer separates badstacks
    # from others, this regular expression parsing will break
    lor_expr = r'%s([^!]+)' % (BAD_STACK_START, )
    flags = re.M | re.S
    matches = re.findall(lor_expr, output, flags=flags)
    bad_stacks = []
    for match in matches:
        if not match:
            continue

        # This assertion's a little more intuitive than the resulting ValueError
        # when the tuple unpack fails
        assert len(match) == 3, "match not in expected format: %r" % (match, )

        bad_stack = {
            'lock 1': match[0].strip(),
            'lock 2': match[1].strip(),
        }
        if not omit_stacks:
            bad_stack['stack'] = match[2].strip() or None
        bad_stacks.append(bad_stack)

    if json_format:
        if json_pretty_print:
            dump_kw = {
                'indent': 4,
                'separators': (',', ': '),
                'sort_keys': True,
            }
        else:
            dump_kw = {}
        json.dump(bad_stacks, sys.stdout, **dump_kw)
        sys.exit(0)

    for bad_stack in bad_stacks:
        key = 'lock 1'
        sys.stdout.write('%s: %s\n' % (key, bad_stack[key], ))
        key = 'lock 2'
        sys.stdout.write('%s: %s\n' % (key, bad_stack[key], ))
        if not omit_stacks:
            key = 'stack'
            sys.stdout.write('%s:\n%s\n' % (key, bad_stack[key], ))
    sys.stdout.flush()


if __name__ == '__main__':
    main()
