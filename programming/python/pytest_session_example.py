#!/usr/bin/env python

from __future__ import print_function

import shutil
import tempfile

import pytest


@pytest.fixture(scope="module")
def ck_attr_dir(request):
    """Set up tests to have temporary test directory in /ifs."""

    # testdir = tempfile.mkdtemp(prefix="attr_test.", dir="/ifs")
    testdir = tempfile.mkdtemp(prefix="attr_test.")

    def ck_attr_dir_teardown():
        """Remove test directory once tests complete."""

        print("Removing testdir: {}".format(testdir))
        shutil.rmtree(testdir)

    request.addfinalizer(ck_attr_dir_teardown)
    return testdir


def print_ck_attr_dirs():
    import subprocess

    print("== print_ck_attr_dirs ==")
    print(
        subprocess.check_output("ls -d /tmp/attr_test.*", shell=True, encoding="utf-8"),
    )
    print("== END ==")


def test_1(ck_attr_dir):
    print("test_1: ck_attr_dir: {}".format(ck_attr_dir))
    print_ck_attr_dirs()


def test_2(ck_attr_dir):
    print("test_2: ck_attr_dir: {}".format(ck_attr_dir))
    print_ck_attr_dirs()
