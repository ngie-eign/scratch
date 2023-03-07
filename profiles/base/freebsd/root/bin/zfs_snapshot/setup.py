#!/usr/bin/env python3

from setuptools import setup

setup(
    name="zfs_snapshot",
    version="0.1",
    description="ZFS snapshot wrapper utility",
    author="Enji Cooper",
    author_email="yaneurabeya@gmail.com",
    url="https://github.com/ngie-eign/python-zfs_snapshot",
    packages=["zfs_snapshot"],
    package_dir={"zfs_snapshot": "src/zfs_snapshot"},
    entry_points={"console_scripts": ["zfs_snapshot=zfs_snapshot.__main__:main"]},
)
