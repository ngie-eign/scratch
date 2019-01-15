#!/usr/bin/env python3

import datetime
import time
import unittest
from unittest.mock import patch

import zfs_snapshot.zfs_snapshot as zfs_snapshot


class TestZfsSnapshot(unittest.TestCase):
    def test_create_snapshot(self):
        """create_snapshot(..)"""

        date_format = "test-1900.01.01d"
        vdev = "a/bogus/vdev"
        with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
            zfs_snapshot.create_snapshot(vdev, date_format)
            snapshot = zfs_snapshot.snapshot_name(vdev, date_format)
            zfs.assert_called_with("snapshot %s" % (snapshot))

    def test_destroy_snapshot(self):
        """destroy_snapshot(..)"""

        snapshot = "a-bogus-snapshot"
        with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
            zfs_snapshot.destroy_snapshot(snapshot)
            zfs.assert_called_with("destroy %s" % (snapshot))

    def test_list_snapshots(self):
        """list_snapshots(..)"""

        test_vdev = "a/bogus/vdev"
        test_snapshots = [
            zfs_snapshot.snapshot_name(test_vdev, "date1"),
            zfs_snapshot.snapshot_name("%s/nested" % (test_vdev), "date1"),
            zfs_snapshot.snapshot_name("i/will/not/match", "date3"),
        ]
        test_input_outputs = [
            ((test_vdev,), test_snapshots[:2]),
            ((test_vdev, False), test_snapshots[0:1]),
            ((test_vdev, True), test_snapshots[:2]),
            (("nonexistent-vdev", False), []),
            (("nonexistent-vdev", True), []),
        ]
        for test_inputs, test_outputs in test_input_outputs:
            with patch("zfs_snapshot.zfs_snapshot.zfs") as zfs:
                zfs.return_value = "\n".join(test_snapshots)
                self.assertEqual(
                    zfs_snapshot.list_snapshots(*test_inputs),
                    test_outputs,
                    "zfs_snapshot.list_snapshots(%r)" % (repr(test_inputs)),
                )

    def test_list_vdevs(self):
        """list_vdevs(..)

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

    #def test_execute_snapshot_policy(self):
    #   raise NotImplementedError()

    def test_is_expired_snapshot(self):
        """is_expired_snapshot(..)"""

        # def is_expired_snapshot(vdev, cutoff, date_format, snapshot):
        date_format = "%Y-%m-%d-%H.%M"
        vdev = "vdev"
        vdev2 = "vdev2"
        nested_vdev = "vdev/nested"

        today = datetime.date.today()

        future_cutoff = today + datetime.timedelta(days=1)
        past_cutoff = today - datetime.timedelta(days=1)

        future_cutoff = future_cutoff.timetuple()
        past_cutoff = past_cutoff.timetuple()

        snapshot = zfs_snapshot.snapshot_name(vdev, time.strftime(date_format))
        snapshot_not_dated = zfs_snapshot.snapshot_name(vdev, "before_reboot")

        self.assertFalse(
            zfs_snapshot.is_expired_snapshot(vdev, future_cutoff, date_format, snapshot)
        )
        self.assertFalse(
            zfs_snapshot.is_expired_snapshot(
                nested_vdev, past_cutoff, date_format, snapshot
            )
        )
        self.assertFalse(
            zfs_snapshot.is_expired_snapshot(
                vdev, past_cutoff, date_format, snapshot_not_dated
            )
        )
        self.assertTrue(
            zfs_snapshot.is_expired_snapshot(vdev, past_cutoff, date_format, snapshot)
        )
