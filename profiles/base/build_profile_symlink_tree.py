#!/usr/bin/env python3

import logging
import os
import os.path


BASE_PROFILE_FILE = "BASE_PROFILE"


class NoBaseProfileException(Exception):
    pass


def build_link_tree_for_path(destdir):
    """Build a link tree with paths relative to common root directory, e.g.,
    ./base/osx/home -> ../../unix/home
    """

    destdir_abs = os.path.abspath(destdir)
    try:
        srcdir = os.readlink(os.path.join(destdir, BASE_PROFILE_FILE))
        srcdir_abs = os.path.abspath(srcdir)
    except FileNotFoundError as err:
        raise NoBaseProfileException(destdir) from err

    for src_file_dir, _, files in os.walk(srcdir, topdown=True):
        destdir_rel = src_file_dir.replace("%s/" % (srcdir), "", 1)
        dest_file_dir = os.path.join(destdir, destdir_rel)
        src_rel_to_dest = os.path.relpath(src_file_dir, dest_file_dir)
        for file_path in files:
            src_file = os.path.join(src_rel_to_dest, file_path)
            dest_file = os.path.join(dest_file_dir, file_path)
            print("%s -> %s" % (src_file, dest_file))
            os.makedirs(dest_file_dir, exist_ok=True)
            try:
                os.remove(dest_file)
            except FileNotFoundError:
                pass
            os.symlink(src_file, dest_file)


def main():
    for path in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if not os.path.isdir(path):
            continue
        try:
            build_link_tree_for_path(path)
        except NoBaseProfileException:
            pass


if __name__ == "__main__":
    main()
