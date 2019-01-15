#!/usr/bin/env python3
"""
Copyright (c) 2019, Enji Cooper
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
import time

from . import zfs_snapshot


SnapshotClass = collections.namedtuple(
    "SnapshotClass",
    # XXX: rework to use the attribute name, instead of a hardcoded index into
    # `time.struct_time`:
    # https://docs.python.org/3/library/time.html#time.struct_time .
    ["mapping_type", "struct_time_index", "lifetime", "date_format_qualifier"],
)

DATE_ELEMENT_SEPARATOR = "."
# The list order matters. See `main(..)` for more details.
SNAPSHOT_CATEGORIES = [
    SnapshotClass(
        mapping_type="year", struct_time_index=0, lifetime=1, date_format_qualifier="Y"
    ),
    SnapshotClass(
        mapping_type="month",
        struct_time_index=1,
        lifetime=12,
        date_format_qualifier="m",
    ),
    SnapshotClass(
        mapping_type="day", struct_time_index=-2, lifetime=30, date_format_qualifier="d"
    ),
    SnapshotClass(
        mapping_type="hour", struct_time_index=3, lifetime=24, date_format_qualifier="H"
    ),
    SnapshotClass(
        mapping_type="minute",
        struct_time_index=5,
        lifetime=15,
        date_format_qualifier="M",
    ),
]

DEFAULT_SNAPSHOT_PERIOD = "hour"
DEFAULT_SNAPSHOT_PREFIX = "auto"


def execute_snapshot_policy(*args, **kwargs):
    """Proxy function for testing"""
    return zfs_snapshot.execute_snapshot_policy(*args, **kwargs)


def list_vdevs(*args, **kwargs):
    """Proxy function for testing"""
    return zfs_snapshot.list_vdevs(*args, **kwargs)


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
    for i, mapping_tuple in enumerate(SNAPSHOT_CATEGORIES):
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

    all_vdevs = list_vdevs()
    value = optarg
    if value in all_vdevs:
        return value
    raise argparse.ArgumentTypeError(
        "Virtual device specified, '%s', does not exist" % (value)
    )


def parse_args(args=None):
    """main"""

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
        default=DEFAULT_SNAPSHOT_PERIOD,
        help=("period with which to manage snapshot policies with"),
        type=period_type,
    )
    parser.add_argument(
        "--snapshot-prefix",
        default=DEFAULT_SNAPSHOT_PREFIX,
        help="prefix to add to a snapshot",
        type=prefix_type,
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="create and destroy snapshots recursively",
    )
    parser.add_argument(
        "--vdev",
        action="append",
        default=[],
        dest="vdevs",
        help="dataset or zvol to snapshot",
        type=vdev_type,
    )
    return parser.parse_args(args)


def main(args=None):
    """self-explanatory"""

    opts = parse_args(args=args)

    # This builds a hierarchical date string in reverse recursive order, e.g.,
    # "2018.09.01" would be "daily".
    #
    # This depends on the ordering of `SNAPSHOT_CATEGORIES`.
    date_format = DATE_ELEMENT_SEPARATOR.join(
        [
            "%" + SNAPSHOT_CATEGORIES[i].date_format_qualifier
            for i in range(opts.snapshot_period + 1)
        ]
    )

    snapshot_cutoff = list(time.localtime())
    struct_tm_offset = SNAPSHOT_CATEGORIES[opts.snapshot_period].struct_time_index
    if opts.lifetime:
        lifetime = opts.lifetime
    else:
        lifetime = SNAPSHOT_CATEGORIES[opts.snapshot_period].lifetime
    snapshot_cutoff[struct_tm_offset] -= lifetime

    now = time.localtime()

    snapshot_suffix = SNAPSHOT_CATEGORIES[opts.snapshot_period].date_format_qualifier

    snapshot_name_format = "%s-%s%s" % (
        opts.snapshot_prefix,
        date_format,
        snapshot_suffix,
    )

    if opts.recursive and opts.vdevs:
        vdevs = []
        for vdev in opts.vdevs:
            vdevs.extend(
                zfs_snapshot.zfs("list -H -o name -r %s" % (vdev)).splitlines()
            )
    elif opts.vdevs:
        vdevs = opts.vdevs
    else:
        vdevs = list_vdevs()

    for vdev in sorted(vdevs, reverse=True):
        execute_snapshot_policy(
            vdev, now, snapshot_cutoff, snapshot_name_format, recursive=opts.recursive
        )


if __name__ == "__main__":
    main()
