#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import argparse
import functools
import multiprocessing  # Oh, how I long for you, `await`...
import os
import pwd
import subprocess
import sys
try:
    from typing import List, Optional  # noqa: F401
except ImportError:
    pass

from humanize.filesize import naturalsize


DEFAULT_CUTOFF = 10
DEFAULT_THRESHOLD = 90


@functools.total_ordering
class Path:

    def __init__(self, path, size):
        # type: (str, int) -> None
        if size < 0:
            raise ValueError("size < 0: %d" % (size))

        self.path = path
        self.size = size

    def __eq__(self, other):
        # type: (Path) -> bool
        return self.size == other.size

    def __lt__(self, other):
        # type: (Path) -> bool
        return self.size < other.size

    def __repr__(self):
        # type: () -> str
        return "%s(%r, %r)" % (self.__class__.__name__, self.path, self.size)


def get_path_info(directory):
    # type: (str) -> Path
    """Get the size of a directory

    :param directory: the directory to get the size for.
    :return: a Path object for `directory`.
    """

    """
    e.g.,

    % sudo du -bs /local/home/ecooper
    4       /local/home/ecooper
    """
    output = subprocess.check_output(["sudo", "du", "-bs", directory]).strip()
    size, path = output.split()

    return Path(path, int(size))


def should_gather_results(directory, min_threshold):
    # type: (str, int) -> bool
    """Should results be gathered for `directory` based on `min_threshold`?

    :param directory: directory to determine whether or not the results should
                      be gathered.
    :param min_threshold: the minimum threshold that should be met in order to
                          gather results.
    :return: True if the results should be gathered; False otherwise.
    """

    """
    e.g.,
    $ df -P /local/home
    Filesystem     1024-blocks       Used Available Capacity Mounted on
    /dev/sdb1       2113645484 2006254976         0     100% /local/home
    """
    output = subprocess.check_output(
        ["df", "-P", directory],
    )

    lines = output.splitlines()
    assert len(lines) == 2, "Output unexpected: %s" % output
    fields = lines[-1].split()[1:3]
    capacity, used = [int(field) for field in fields]

    # print(capacity, used)

    return min_threshold < 100 * used / capacity


def gather_path_info_for_root(root):
    # type: (str) -> List(Path)
    """

    """

    subdirs = [
        os.path.join(root, subdir)
        for subdir in os.listdir(root) if subdir not in (".", "..")
    ]

    pool = multiprocessing.Pool()
    try:
        results = pool.map_async(get_path_info, subdirs)
        path_info_objs = [path_obj for path_obj in results.get()]
        pool.close()
    except:
        pool.terminate()
        raise
    finally:
        pool.join()

    return path_info_objs


def main(argv=None):
    # type: Optional[List[str]] -> None
    """main"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cutoff", default=DEFAULT_CUTOFF, type=int,
    )
    parser.add_argument(
        "--threshold", default=DEFAULT_THRESHOLD, type=int,
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
        sys.exit(0)

    homedirs_with_sizes = gather_path_info_for_root(args.rootdir)
    homedirs_with_sizes_sorted = sorted(homedirs_with_sizes, reverse=True)

    # print(homedirs_with_sizes_sorted)
    max_elems = min(args.cutoff, len(homedirs_with_sizes))
    for i, path_obj in enumerate(homedirs_with_sizes_sorted[:max_elems], 1):
        owner = os.stat(path_obj.path).st_uid
        try:
            pwent = pwd.getpwuid(owner)
        except KeyError:
            pass
        else:
            owner = pwent.pw_name

        subdir_size_humanized = naturalsize(path_obj.size, binary=True)
        print("%2d. %80s %40s %s" % (
            i, path_obj.path, owner, subdir_size_humanized
        ))


if __name__ == "__main__":
    main()
