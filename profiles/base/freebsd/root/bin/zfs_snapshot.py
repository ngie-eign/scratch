#!/usr/bin/env python3
"""
Copyright (c) 2017-2018, Enji Cooper
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

import argparse
import collections
import shlex
import subprocess
import time


SnapshotMapping = collections.namedtuple(
    "SnapshotMapping",
    # XXX: struct_time_index might not be needed with py3.
    ["mapping_type", "struct_time_index", "lifetime", "date_format_qualifier"],
)


ALL_VDEVS = []
SNAPSHOT_MAPPINGS = [
    SnapshotMapping(
        mapping_type="year", struct_time_index=0, lifetime=1, date_format_qualifier="Y"
    ),
    SnapshotMapping(
        mapping_type="month",
        struct_time_index=1,
        lifetime=12,
        date_format_qualifier="m",
    ),
    SnapshotMapping(
        mapping_type="day", struct_time_index=-2, lifetime=30, date_format_qualifier="d"
    ),
    SnapshotMapping(
        mapping_type="hour", struct_time_index=3, lifetime=24, date_format_qualifier="H"
    ),
    SnapshotMapping(
        mapping_type="minute",
        struct_time_index=5,
        lifetime=15,
        date_format_qualifier="M",
    ),
]
SEPARATOR = "."
SNAPSHOTS_LIST = []
ZFS = "/sbin/zfs"


def zfs(arg_str, fake=False):
    """A command through zfs(8).

    :Parameters:
        arg_str: a flat string with a list of arguments to pass to zfs(8),
                 e.g. -t snapshot.
        fake:    fake the command call.
    """

    if fake:
        print("Would execute: %s %s" % (ZFS, arg_str))
        return ""
    output = subprocess.check_output([ZFS] + shlex.split(arg_str))
    try:
        return str(output, encoding="utf-8")
    except TypeError:
        return output


def create_snapshot(vdev, date_format):
    """Create a snapshot for a vdev with a given date format.

    :Parameters:
         vdev:        name of a vdev to take a snapshot with.
         date_format: strftime(3) compatible date format to assign to the
                      snapshot.
    """

    zfs("snapshot {}@{}".format(vdev, date_format))


def destroy_snapshot(snapshot):
    """Destroy a snapshot

    :Parameters:
        snapshot: name of the snapshot to destroy.
    """

    zfs("destroy {}".format(snapshot))


def list_vdevs():
    """Return all vdevs.

    :Raises:
        ValueError: no vdevs could be found.

    :Returns:
        A list of available vdevs.
    """

    vdevs = zfs("list -H -t filesystem,volume -o name").split()
    if not vdevs:
        raise ValueError("no vdevs found on system")
    return vdevs


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

        if snapshot.startswith("@" + vdev):
            return True
        if recursive and snapshot.startswith("/" + vdev):
            return True
        return False

    if not SNAPSHOTS_LIST:
        SNAPSHOTS_LIST = zfs("list -H -t snapshot -o name").splitlines()

    return [snap for snap in SNAPSHOTS_LIST if filter_function(snap)]


def find_expired_snapshots(vdev, cutoff, date_format, snapshot):
    """Take a snapshot string, unmarshall the date, and determine if it's
       eligible for destruction.

    :Parameters:
         vdev:        name of the vdev to execute the snapshotting policy
                      (creation/deletion) on.
         cutoff:      any snapshots created before this time are nuked. This
                      is a tuple, resembling a time.struct_tm.
         date_format: a strftime(3) compatible date format to look for/destroy
                      snapshots with.
         snapshot: snapshot name.

    :Returns:
       The name of the snapshot if expired; None otherwise.
    """

    try:
        snapshot_time = time.strptime(snapshot, "{}@{}".format(vdev, date_format))
        if snapshot_time < time.struct_time(cutoff):
            return snapshot
    except ValueError:
        pass
    return None


def execute_snapshot_policy(vdev, now, cutoff, date_format, recursive=True):
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

    expired_snapshots = [
        expired_snapshot
        for expired_snapshot in snapshots
        if find_expired_snapshots(vdev, cutoff, date_format, expired_snapshot)
    ]
    for snapshot in sorted(expired_snapshots, reverse=True):
        # Destroy snapshots as needed, reverse order so the snapshots will
        # be destroyed in order.
        destroy_snapshot(snapshot)

    create_snapshot(vdev, time.strftime(date_format, now))


def lifetime_type(optarg):
    """Validate --lifetime to ensure that it's > 0.
    """

    value = int(optarg)
    if value <= 0:
        raise argparse.ArgumentTypeError(
            "Lifetime must be an integer value greater than 0"
        )
    return value


def period_type(optarg):
    """Validate --snapshot-period to ensure that the value passed is valid."""

    value = optarg.lower()
    for i, mapping_tuple in enumerate(SNAPSHOT_MAPPINGS):
        if mapping_tuple.mapping_type == value:
            return i
    raise argparse.ArgumentTypeError("Invalid --snapshot-period: %s" % (optarg))


def prefix_type(optarg):
    """Validate --prefix to ensure that it's a non-nul string"""

    value = optarg
    if value:
        return value
    raise argparse.ArgumentTypeError("Snapshot prefix must be a non-zero length string")


def vdev_type(optarg):
    """Validate --vdev to ensure that the vdev provided exist(ed) at
       the time the script was executed.
    """

    value = optarg
    if value in ALL_VDEVS:
        return value
    raise argparse.ArgumentTypeError(
        "Dataset specified, '%s' does not exist" % (value,)
    )


def main(args=None):
    """main"""

    global ALL_VDEVS

    ALL_VDEVS = list_vdevs()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lifetime",
        help=(
            "lifetime (number of snapshots) to keep of a "
            "vdev; the value is relative to the number of "
            '"periods".'
        ),
        type=lifetime_type,
    )
    parser.add_argument(
        "--snapshot-period",
        default="hour",
        help=("period with which to manage snapshot policies " "with"),
        type=period_type,
    )
    parser.add_argument(
        "--snapshot-prefix",
        default="auto",
        help="prefix to add to a snapshot",
        type=prefix_type,
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="create and destroy snapshots recursively",
    )
    parser.add_argument(
        "--snapshot-suffix",
        default="",
        help=(
            "suffix to add to the end of the snapshot; "
            "defaults to the strdate(3)-format qualifier"
        ),
    )
    parser.add_argument(
        "--vdev",
        action="append",
        default=[],
        dest="vdevs",
        help="dataset or zvol to snapshot",
        type=vdev_type,
    )

    opts = parser.parse_args(args)

    date_format = SEPARATOR.join(
        [
            "%" + SNAPSHOT_MAPPINGS[i].date_format_qualifier
            for i in range(opts.snapshot_period + 1)
        ]
    )

    snapshot_cutoff = list(time.localtime())
    struct_tm_offset = SNAPSHOT_MAPPINGS[opts.snapshot_period].struct_time_index
    if opts.lifetime:
        lifetime = opts.lifetime
    else:
        lifetime = SNAPSHOT_MAPPINGS[opts.snapshot_period].lifetime
    snapshot_cutoff[struct_tm_offset] -= lifetime

    now = time.localtime()

    if opts.snapshot_suffix:
        snapshot_suffix = opts.snapshot_suffix
    else:
        snapshot_suffix = SNAPSHOT_MAPPINGS[opts.snapshot_period].date_format_qualifier

    date_format = "%s-%s%s" % (opts.snapshot_prefix, date_format, snapshot_suffix)

    if opts.vdevs:
        vdevs = opts.vdevs
        if opts.recursive:
            vdevs = [vdev for vdev in ALL_VDEVS if vdev.startswith(vdev + "/")]
    else:
        vdevs = ALL_VDEVS

    for vdev in sorted(vdevs, reverse=True):
        execute_snapshot_policy(
            vdev, now, snapshot_cutoff, date_format, recursive=opts.recursive
        )


if __name__ == "__main__":
    main()
