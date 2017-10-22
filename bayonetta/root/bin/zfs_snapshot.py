#!/usr/bin/env python
"""
Copyright (c) 2012, Ngie Cooper
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import optparse
import shlex
import subprocess
import sys
import time


SEPARATOR = '.'
ZFS = '/sbin/zfs'


def zfs(arg_str, fake=False):
    """A command through zfs(8).

    :Parameters:
        arg_str: a flat string with a list of arguments to pass to zfs(8),
                 e.g. -t snapshot.
        fake:    fake the command call.
    """

    if fake:
        sys.stdout.write('Would execute: %s %s\n' % (ZFS, arg_str, ))
        sys.stdout.flush()
        return ''
    return subprocess.check_output([ZFS] + shlex.split(arg_str))


def create_snapshot(vdev, date_format):
    """Create a snapshot for a vdev with a given date format.

    :Parameters:
         vdev:        name of a vdev to take a snapshot with.
         date_format: strftime(3) compatible date format to assign to the
                      snapshot.
    """

    zfs('snapshot %s@%s' % (vdev, date_format, ))


def destroy_snapshot(snapshot):
    """Destroy a snapshot

    :Parameters:
        snapshot: name of the snapshot to destroy.
    """

    zfs('destroy %s' % (snapshot, ))


def list_vdevs():
    """Return all vdevs.

    :Raises:
        ValueError: no vdevs could be found.

    :Returns:
        A list of available vdevs.
    """

    vdevs = zfs('list -H -t filesystem,volume -o name').split()
    if not vdevs:
        raise ValueError('no vdevs found on system')
    return vdevs


SNAPSHOTS_LIST = []


def list_snapshots(vdev, recursive=True):
    """Get a list of ZFS snapshots for a given vdev

    :Parameters:
        vdev:      a vdev to grab snapshots for.
        recursive: list snapshot(s) for the parent and child vdevs.

    :Returns:
        A list of 0 or more snapshots
    """

    global SNAPSHOTS_LIST

    def filter_function(snapshot):
        """Filter by parent vdev or nested vdev (depending on how the
           function was called).

        :Parameters:
            snapshot: full snapshot name
        """

        if (snapshot.startswith(vdev + '@') or
            (recursive and snapshot.startswith(vdev + '/'))):
            return True
        return False

    if not SNAPSHOTS_LIST:
        SNAPSHOTS_LIST = zfs('list -H -t snapshot -o name').splitlines()

    return filter(filter_function, SNAPSHOTS_LIST)


def execute_snapshot_policy(vdev,
                            now,
                            cutoff,
                            date_format,
                            recursive=True,
                            ):
    """Execute snapshot policy on a vdev -- destroying as necessary and
       creating a snapshot at the end.

    :Parameters:
         vdev:        name of the vdev to execute the snapshotting policy
                      (creation/deletion) on.
         now:         new time to snapshot against. This should be the time
                      that the script execution was started (e.g. a stable
                      value).
         cutoff:      any snapshots created before this time are nuked. This
                      is a tuple, resembling a time.struct_tm.
         date_format: a strftime(3) compatible date format to look for/destroy
                      snapshots with.
         recursive:   execute zfs snapshot create recursively.
    """

    snapshots = list_snapshots(vdev, recursive=recursive)

    def _find_expired_snapshots(snapshot):
        """Take a snapshot string, unmarshall the date, and determine if it's
           eligible for destruction.

        :Parameters:
           snapshot: snapshot name.

        :Returns:
           The name of the snapshot if expired; None otherwise.
        """

        try:
            snapshot_time = time.strptime(snapshot,
                                          '%s@%s' % (vdev, date_format, ))
            if time.mktime(snapshot_time) < time.mktime(cutoff):
                return snapshot
        except ValueError:
            pass
        return None

    expired_snapshots = filter(_find_expired_snapshots, snapshots)
    for snapshot in sorted(expired_snapshots, reverse=True):
        # Destroy snapshots as needed, reverse order so the snapshots will
        # be destroyed in order.
        destroy_snapshot(snapshot)

    create_snapshot(vdev, time.strftime(date_format, now))


def main(args):
    """main"""

    def validate_vdev(option, opt, value, parser):
        """Validate --vdev to ensure that the vdev provided exist(ed) at
           the time the script was executed.
        """

        if value not in all_vdevs:
            raise optparse.OptionValueError('Dataset specified (%s) does not '
                                            'exist' % (value, ))
        parser.values.vdevs.append(value)

    def validate_lifetime(option, opt, value, parser):
        """Validate --lifetime to ensure that it's > 0.
        """

        if value <= 0:
            raise optparse.OptionValueError('Lifetime must be an integer '
                                            'value greater than 0')
        parser.values.lifetime = value

    def validate_period(option, opt, value, parser):
        """Validate --period to ensure that the value passed is valid."""

        mapping_names = [snapshot_type.lower() for snapshot_type, __, __, __ in
                                                          snapshot_mappings]

        if value not in mapping_names:
            raise optparse.OptionValueError('Period must be one of the '
                                            'following: %s' %
                                            (', '.join(mapping_names), ))
        parser.values.period = mapping_names.index(value)

    def validate_prefix(option, opt, value, parser):
        """Validate --prefix to ensure that it's """

        if not value:
            raise optparse.OptionValueError('Snapshot prefix must be a '
                                            'non-zero length string')
        parser.values.prefix = value

    all_vdevs = list_vdevs()

    snapshot_mappings = [
        # Type, time.struct_time index, sane lifetime, date format qualifier
        ('year',    0, 10, 'Y', ),
        ('Month',   1, 12, 'm', ),
        ('day',    -2, 30, 'd', ),
        ('hour',    3, 24, 'H', ),
        ('minute',  5, 15, 'M', ),
    ]

    parser = optparse.OptionParser()
    parser.add_option('-l', '--lifetime',
                      action='callback',
                      callback=validate_lifetime,
                      dest='lifetime',
                      help=('lifetime (number of snapshots) to keep of a '
                            'vdev; is "period" specific'),
                      type='int',
                      )
    parser.add_option('-p', '--snapshot-period',
                      action='callback',
                      callback=validate_period,
                      default=3,
                      dest='period',
                      help=('period with which to manage snapshot policies '
                            'with.'),
                      type='string',
                      )
    parser.add_option('-P', '--snapshot-prefix',
                      action='callback',
                      callback=validate_prefix,
                      default='auto',
                      dest='prefix',
                      help='prefix to add to a snapshot',
                      type='string',
                      )
    parser.add_option('-r', '--recursive',
                      action='store_true',
                      dest='recursive',
                      help='create and destroy snapshots recursively',
                      )
    parser.add_option('-s', '--snapshot-suffix',
                      default='',
                      dest='snapshot_suffix',
                      help=('suffix to add to the end of the snapshot; '
                            'defaults to the first character of the period'),
                      type='string',
                      )
    parser.add_option('-V', '--vdev',
                      action='callback',
                      callback=validate_vdev,
                      default=[],
                      dest='vdevs',
                      help='dataset or zvol to snapshot',
                      type='string',
                      )

    opts, __ = parser.parse_args(args)

    date_format = SEPARATOR.join(['%' + snapshot_mappings[i][-1] for i in
                                                      range(opts.period + 1)])

    snapshot_cutoff = list(time.localtime())
    struct_tm_offset = snapshot_mappings[opts.period][1]
    if opts.lifetime:
        lifetime = opts.lifetime
    else:
        __, __, lifetime, __ = snapshot_mappings[opts.period]
    snapshot_cutoff[struct_tm_offset] -= lifetime

    now = time.localtime()

    if opts.snapshot_suffix:
        snapshot_suffix = opts.snapshot_suffix
    else:
        snapshot_suffix = snapshot_mappings[opts.period][0][0]

    date_format = '%s-%s%s' % (opts.prefix, date_format, snapshot_suffix, )

    if opts.vdevs:
        vdevs = opts.vdevs
        if opts.recursive:
            vdevs = filter(lambda vdev: vdev.startswith('%s/' % (vdev, )),
                                                        all_vdevs)
    else:
        vdevs = all_vdevs

    for vdev in sorted(vdevs, reverse=True):

        execute_snapshot_policy(vdev,
                                now,
                                snapshot_cutoff,
                                date_format,
                                recursive=opts.recursive,
                                )


if __name__ == '__main__':
    main(sys.argv)
