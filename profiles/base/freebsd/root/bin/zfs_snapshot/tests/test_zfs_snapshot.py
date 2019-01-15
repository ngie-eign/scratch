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

import datetime
import time
import unittest
from unittest.mock import call, patch

import zfs_snapshot.zfs_snapshot as zfs_snapshot


def patch_zfs_snapshot(rel_path):
    return patch("zfs_snapshot.zfs_snapshot.%s" % (rel_path))


class TestZfsSnapshot(unittest.TestCase):
    @staticmethod
    def test_create_snapshot():
        """create_snapshot(..)"""

        date_format = "test-1900.01.01d"
        vdev = "a/bogus/vdev"
        with patch_zfs_snapshot("zfs") as zfs:
            zfs_snapshot.create_snapshot(vdev, date_format)
            snapshot = zfs_snapshot.snapshot_name(vdev, date_format)
            zfs.assert_called_with("snapshot %s" % (snapshot))

    @staticmethod
    def test_destroy_snapshot():
        """destroy_snapshot(..)"""

        snapshot = "a-bogus-snapshot"
        with patch_zfs_snapshot("zfs") as zfs:
            zfs_snapshot.destroy_snapshot(snapshot)
            zfs.assert_called_with("destroy %s" % (snapshot))

    def test_list_snapshots(self):
        """list_snapshots(..)"""

        test_vdev = "a/bogus/vdev"
        test_snapshots = [
            zfs_snapshot.snapshot_name(test_vdev, "date1"),
            zfs_snapshot.snapshot_name("%s/nested" % (test_vdev), "date1"),
            zfs_snapshot.snapshot_name("%s/nested" % (test_vdev), "date2"),
            zfs_snapshot.snapshot_name("%s.trailer", "date1"),
        ]
        test_input_outputs = [
            ((test_vdev,), test_snapshots[:3]),
            ((test_vdev, False), test_snapshots[0:1]),
            ((test_vdev, True), test_snapshots[:3]),
        ]
        for test_inputs, test_outputs in test_input_outputs:
            if len(test_inputs) == 1:
                recursive = True
            else:
                recursive = test_inputs[-1]
            with patch_zfs_snapshot("zfs") as zfs:
                zfs.return_value = "\n".join(
                    [
                        snapshot
                        for snapshot in test_snapshots
                        if snapshot.startswith(
                            test_vdev + zfs_snapshot.SNAPSHOT_SEPARATOR
                        )
                        or (recursive and snapshot.startswith(test_vdev + "/"))
                    ]
                )
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
            with patch_zfs_snapshot("zfs") as zfs:
                zfs.return_value = "\n".join(test_vdev_list)
                self.assertEqual(zfs_snapshot.list_vdevs(), test_vdev_list)

        with patch_zfs_snapshot("zfs") as zfs:
            zfs.return_value = ""
            with self.assertRaises(ValueError):
                zfs_snapshot.list_vdevs()

    @staticmethod
    def test_execute_snapshot_policy():
        """execute_snapshot_policy(..)

        This test method is a functional smoke test, more or less.
        """

        test_vdev = "vdev"
        test_cutoff = datetime.date.today().timetuple()
        test_date_format = "%Y-%m-%d-%H.%M"
        now = time.localtime()

        test_snapshots = [
            zfs_snapshot.snapshot_name(test_vdev, "date1"),
            zfs_snapshot.snapshot_name("%s/nested" % (test_vdev), "date1"),
            zfs_snapshot.snapshot_name("i/will/not/match", "date3"),
        ]
        num_snapshots = len(test_snapshots)

        with patch_zfs_snapshot(
            "create_snapshot"
        ) as create_snapshot, patch_zfs_snapshot(
            "destroy_snapshot"
        ) as destroy_snapshot, patch_zfs_snapshot(
            "is_destroyable_snapshot"
        ) as is_destroyable_snapshot, patch_zfs_snapshot(
            "list_snapshots"
        ) as list_snapshots:
            list_snapshots.return_value = []
            zfs_snapshot.execute_snapshot_policy(
                test_vdev, now, test_cutoff, test_date_format
            )
            # No snapshots means none of these methods (minus create_snapshot)
            # should have been called
            is_destroyable_snapshot.assert_not_called()
            destroy_snapshot.assert_not_called()
            create_snapshot.assert_called_with(
                test_vdev, time.strftime(test_date_format, now)
            )

        # Verify that no snapshots are destroyed if they haven't expired.
        with patch_zfs_snapshot(
            "create_snapshot"
        ) as create_snapshot, patch_zfs_snapshot(
            "destroy_snapshot"
        ) as destroy_snapshot, patch_zfs_snapshot(
            "is_destroyable_snapshot"
        ) as is_destroyable_snapshot, patch_zfs_snapshot(
            "list_snapshots"
        ) as list_snapshots:
            list_snapshots.return_value = test_snapshots
            is_destroyable_snapshot.side_effect = [False] * num_snapshots
            zfs_snapshot.execute_snapshot_policy(
                test_vdev, now, test_cutoff, test_date_format
            )
            destroy_snapshot.assert_not_called()
            create_snapshot.assert_called_with(
                test_vdev, time.strftime(test_date_format, now)
            )

        # Verify that a single snapshot is destroyed because it has expired.
        with patch_zfs_snapshot(
            "create_snapshot"
        ) as create_snapshot, patch_zfs_snapshot(
            "destroy_snapshot"
        ) as destroy_snapshot, patch_zfs_snapshot(
            "is_destroyable_snapshot"
        ) as is_destroyable_snapshot, patch_zfs_snapshot(
            "list_snapshots"
        ) as list_snapshots:
            list_snapshots.return_value = test_snapshots
            is_destroyable_snapshot.side_effect = [True] + [False] * (num_snapshots - 1)
            zfs_snapshot.execute_snapshot_policy(
                test_vdev, now, test_cutoff, test_date_format
            )
            destroy_snapshot.assert_called_with(test_snapshots[0])
            create_snapshot.assert_called_with(
                test_vdev, time.strftime(test_date_format, now)
            )

        # Ensure that expired snapshots are destroyed in reverse order.
        #
        # This is needed, otherwise, zfs will fail stating that the parent
        # dataset still has snapshot references that has not been destroyed
        # in child datasets
        with patch_zfs_snapshot(
            "create_snapshot"
        ) as create_snapshot, patch_zfs_snapshot(
            "destroy_snapshot"
        ) as destroy_snapshot, patch_zfs_snapshot(
            "is_destroyable_snapshot"
        ) as is_destroyable_snapshot, patch_zfs_snapshot(
            "list_snapshots"
        ) as list_snapshots:
            list_snapshots.return_value = test_snapshots
            is_destroyable_snapshot.side_effect = [True] * 2 + [False] * (
                num_snapshots - 2
            )
            zfs_snapshot.execute_snapshot_policy(
                test_vdev, now, test_cutoff, test_date_format
            )
            destroy_snapshot.assert_has_calls(
                [
                    call(snapshot)
                    for snapshot in sorted(test_snapshots[:2], reverse=True)
                ]
            )
            create_snapshot.assert_called_with(
                test_vdev, time.strftime(test_date_format, now)
            )

    def test_is_destroyable_snapshot(self):
        """is_destroyable_snapshot(..)"""

        # def is_destroyable_snapshot(vdev, cutoff, date_format, snapshot):
        date_format = "%Y-%m-%d-%H.%M"
        vdev = "vdev"
        nested_vdev = "vdev/nested"

        today = datetime.date.today()

        future_cutoff = today + datetime.timedelta(days=1)
        past_cutoff = today - datetime.timedelta(days=1)

        future_cutoff = future_cutoff.timetuple()
        past_cutoff = past_cutoff.timetuple()

        snapshot = zfs_snapshot.snapshot_name(vdev, time.strftime(date_format))
        snapshot_not_dated = zfs_snapshot.snapshot_name(vdev, "before_reboot")

        self.assertTrue(
            zfs_snapshot.is_destroyable_snapshot(
                vdev, future_cutoff, date_format, snapshot
            )
        )
        self.assertFalse(
            zfs_snapshot.is_destroyable_snapshot(
                nested_vdev, past_cutoff, date_format, snapshot
            )
        )
        self.assertFalse(
            zfs_snapshot.is_destroyable_snapshot(
                vdev, past_cutoff, date_format, snapshot_not_dated
            )
        )
        self.assertFalse(
            zfs_snapshot.is_destroyable_snapshot(
                vdev, past_cutoff, date_format, snapshot
            )
        )
