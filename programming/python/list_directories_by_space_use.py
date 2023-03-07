#!/usr/bin/env python3

import argparse
import functools
import multiprocessing  # Oh, how I long for you, `await`...
import os
import pathlib
import pwd
import subprocess
import sys
from os import PathLike
from typing import Any
from typing import Optional
from typing import Union

from humanize.filesize import naturalsize


DEFAULT_CUTOFF = 10
DEFAULT_THRESHOLD = 90

PathIsh = Union[PathLike, str]


@functools.total_ordering
class ComparablePath:
    def __init__(self, path: PathIsh, size: int):
        if size < 0:
            raise ValueError(f"size < 0: {size:d}")

        self.path = path
        self.size = size

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ComparablePath):
            return NotImplemented
        return self.size == other.size

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, ComparablePath):
            return NotImplemented
        return self.size < other.size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path!r}, {self.size})"


def get_path_info(directory: PathIsh) -> ComparablePath:
    """Get the size of a directory.

    :param directory: the directory to get the size for.
    :return: a ComparablePath object for `directory`.
    """

    #
    # e.g.,
    #
    # % sudo du -sB 1 /local/home/ecooper
    # 4       /local/home/ecooper

    output = subprocess.check_output(
        ["sudo", "du", "-sB", "1", str(directory)],
        text=True,
    )
    size, path = output.strip().split(maxsplit=2)

    return ComparablePath(path, int(size))


def should_gather_results(directory: PathIsh, min_threshold: int) -> bool:
    """Should results be gathered for `directory` based on `min_threshold`?

    :param directory: directory to determine whether or not the results should
                      be gathered.
    :param min_threshold: the minimum threshold that should be met in order to
                          gather results.
    :return: True if the results should be gathered; False otherwise.
    """

    # e.g.,
    # $ df -P /local/home
    # Filesystem     1024-blocks       Used Available Capacity Mounted on
    # /dev/sdb1       2113645484 2006254976         0     100% /local/home
    output = subprocess.check_output(["df", "-P", directory], text=True)

    lines = output.splitlines()
    assert len(lines) == 2, f"Output unexpected: {output}"
    fields = lines[-1].split()[1:3]
    capacity, used = [int(field) for field in fields]

    # print(capacity, used)

    return min_threshold < 100 * used / capacity


def gather_path_info_for_root(root: pathlib.Path) -> list[ComparablePath]:
    subdirs = list(root.iterdir())

    with multiprocessing.Pool() as pool:
        results = pool.map_async(get_path_info, subdirs)
        path_info_objs = list(results.get())
    return path_info_objs


def main(argv: Optional[list[str]] = None) -> int:
    """Eponymous main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cutoff",
        default=DEFAULT_CUTOFF,
        type=int,
    )
    parser.add_argument(
        "--threshold",
        default=DEFAULT_THRESHOLD,
        type=int,
    )
    parser.add_argument(
        "rootdir",
    )

    args = parser.parse_args(args=argv)

    # Overall implementation/process:
    #
    # 1. Run `df -P` on $HOME/.. . If the space available is higher than a
    #    threshold, exit.
    #
    # 2. Iterate through all of the directories, using `os.listdir()` and
    #    sort them by size.

    if not should_gather_results(args.rootdir, args.threshold):
        return 0

    homedirs_with_sizes = gather_path_info_for_root(pathlib.Path(args.rootdir))
    homedirs_with_sizes_sorted = sorted(homedirs_with_sizes, reverse=True)

    # print(homedirs_with_sizes_sorted)
    max_elems = min(args.cutoff, len(homedirs_with_sizes))
    for i, path_obj in enumerate(homedirs_with_sizes_sorted[:max_elems], 1):
        owner_uid = os.stat(path_obj.path).st_uid
        try:
            pwent = pwd.getpwuid(owner_uid)
        except KeyError:
            owner = str(owner_uid)
        else:
            owner = pwent.pw_name

        subdir_size_humanized = naturalsize(path_obj.size, binary=True)
        print(f"{i:2d}. {path_obj.path:80s} {owner:40s} {subdir_size_humanized}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
