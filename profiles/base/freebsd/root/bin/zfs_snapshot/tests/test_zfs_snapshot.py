#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import zfs_snapshot.zfs_snapshot as zfs_snapshot


class TestZfsSnapshot(unittest.TestCase):

    def test_create_snapshot(self):
        date_format = "test-1900.01.01d"
        vdev = "a/bogus/vdev"
        with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
            zfs_snapshot.create_snapshot(vdev, date_format)
            zfs.assert_called_with("snapshot {}@{}".format(vdev, date_format))

    def test_destroy_snapshot(self):
        snapshot = "a-bogus-snapshot"
        with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
            zfs_snapshot.destroy_snapshot(snapshot)
            zfs.assert_called_with("destroy {}".format(snapshot))

    def test_list_snapshots(self):
        test_vdev = "a/bogus/vdev"
        test_snapshots = [
            "{}@date1".format(test_vdev),
            "{}/nested@date2".format(test_vdev),
            "i/will/not/match@date3"
        ]
        test_input_outputs = [
            ((test_vdev, ), test_snapshots[:2]),
            ((test_vdev, False), test_snapshots[0:1]),
            ((test_vdev, True), test_snapshots[:2]),
            (("nonexistent-vdev", False), []),
            (("nonexistent-vdev", True), [])
        ]
        for test_inputs, test_outputs in test_input_outputs:
            with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
                zfs.return_value = "\n".join(test_snapshots)
                self.assertEqual(
                    zfs_snapshot.list_snapshots(*test_inputs),
                    test_outputs,
                    "zfs_snapshot.list_snapshots(%r)" % (repr(test_inputs))
                )

    def test_list_vdevs(self):
        """list_vdevs(..) positive testcase

        `list_vdevs(..)` should omit one or more vdevs in a list format, or
        raise a ValueError if none could be listed.
        """
        test_vdev_sets = [["vdev"], ["vdev1", "vdev2", "vdev3/sub-vdev"]]

        for test_vdev_list in test_vdev_sets:
            with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
                zfs.return_value = "\n".join(test_vdev_list)
                self.assertEqual(zfs_snapshot.list_vdevs(), test_vdev_list)

        with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
            zfs.return_value = ""
            with self.assertRaises(ValueError):
                zfs_snapshot.list_vdevs()
