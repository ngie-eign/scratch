#!/usr/bin/env python3
"""
Copyright (c) 2019-2023, Enji Cooper
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
import datetime
from typing import Any
from typing import Optional
from typing import Union

from . import zfs_snapshot


SnapshotClass = collections.namedtuple(
    "SnapshotClass", ["name", "lifetime", "date_format_qualifier"]
)

DATE_ELEMENT_SEPARATOR = "."
NOW = datetime.datetime.now()
# These are very much approximations of reality.
#
# XXX: I really wish `dateutil.relativedelta(..)` actually worked reliably (it
# was screwing up the difference between a datetime and the value in the
# relativedelta).
WEEKS_IN_A_MONTH = 4
WEEKS_IN_A_YEAR = 52
# The list order matters. See `main(..)` for more details.
SNAPSHOT_CATEGORIES = [
    SnapshotClass(
        name="years",
        lifetime=datetime.timedelta(weeks=2 * WEEKS_IN_A_YEAR),
        date_format_qualifier="Y",
    ),
    SnapshotClass(
        name="months",
        lifetime=datetime.timedelta(weeks=1 * WEEKS_IN_A_YEAR),
        date_format_qualifier="m",
    ),
    SnapshotClass(
        name="days",
        lifetime=datetime.timedelta(weeks=1 * WEEKS_IN_A_MONTH),
        date_format_qualifier="d",
    ),
    SnapshotClass(
        name="hours", lifetime=datetime.timedelta(days=1), date_format_qualifier="H"
    ),
]
DEFAULT_SNAPSHOT_PERIOD = "hours"
DEFAULT_SNAPSHOT_PREFIX = "auto"


def execute_snapshot_policy(*args: Any, **kwargs: Any) -> None:
    """Proxy function for testing"""
    return zfs_snapshot.execute_snapshot_policy(*args, **kwargs)


def list_vdevs(*args: Any, **kwargs: Any) -> list[str]:
    """Proxy function for testing."""
    return zfs_snapshot.list_vdevs(*args, **kwargs)


def lifetime_type(optarg: str) -> int:
    """Validate --lifetime to ensure that it's > 0."""

    value = int(optarg)
    if value <= 0:
        raise argparse.ArgumentTypeError(
            "Lifetime must be an integer value greater than 0"
        )
    return value


def period_type(optarg: str) -> int:
    """Validate --snapshot-period to ensure that the value passed is valid."""

    value = optarg.lower()
    for i, mapping_tuple in enumerate(SNAPSHOT_CATEGORIES):
        if mapping_tuple.name == value:
            return i
    raise argparse.ArgumentTypeError("Invalid --snapshot-period: %s" % (optarg))


def prefix_type(optarg: str) -> str:
    """Validate --prefix to ensure that it's a non-nul string"""

    value = optarg
    if value:
        return value
    raise argparse.ArgumentTypeError("Snapshot prefix must be a non-zero length string")


def vdev_type(optarg: str) -> str:
    """Validate --vdev.

    This ensures that the vdev provided on the CLI exist(ed) at the time the script was
    executed.
    """

    all_vdevs = list_vdevs()
    value = optarg
    if value in all_vdevs:
        return value
    raise argparse.ArgumentTypeError(
        "Virtual device specified, '%s', does not exist" % (value)
    )


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
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


def compute_cutoff(
    snapshot_category: SnapshotClass,
    lifetime_override: Union[int, float],
) -> datetime.datetime:
    if lifetime_override:
        category_name = snapshot_category.name
        if category_name == "years":
            category_name = "weeks"
            lifetime_override *= WEEKS_IN_A_YEAR
        elif category_name == "months":
            category_name = "weeks"
            lifetime_override *= WEEKS_IN_A_MONTH
        lifetime = datetime.timedelta(**{category_name: lifetime_override})
    else:
        lifetime = snapshot_category.lifetime
    return NOW - lifetime


def compute_vdevs(vdevs: list[str], recursive: bool) -> list[str]:
    if recursive and vdevs:
        target_vdevs = []
        for vdev in vdevs:
            target_vdevs.extend(
                zfs_snapshot.zfs(f"list -H -o name -r {vdev}").splitlines()
            )
        return target_vdevs
    return vdevs or list_vdevs()


def main(args: Optional[list[str]] = None) -> None:
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

    snapshot_category = SNAPSHOT_CATEGORIES[opts.snapshot_period]
    snapshot_suffix = snapshot_category.date_format_qualifier
    snapshot_name_format = "%s-%s%s" % (
        opts.snapshot_prefix,
        date_format,
        snapshot_suffix,
    )
    snapshot_cutoff = compute_cutoff(snapshot_category, opts.lifetime)
    vdevs = compute_vdevs(opts.vdevs, opts.recursive)

    for vdev in sorted(vdevs, reverse=True):
        execute_snapshot_policy(
            vdev,
            NOW.timetuple(),
            snapshot_cutoff.timetuple(),
            snapshot_name_format,
            recursive=opts.recursive,
        )
