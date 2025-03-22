#!/usr/bin/env python3
"""
Copyright (c) 2018, Enji Cooper
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

import unittest
from unittest.mock import call, patch

from dateutil.relativedelta import relativedelta

from zfs_snapshot.__main__ import (
    compute_cutoff,
    compute_vdevs,
    parse_args,
    period_type,
    DEFAULT_SNAPSHOT_PERIOD,
    DEFAULT_SNAPSHOT_PREFIX,
    NOW,
    SNAPSHOT_CATEGORIES,
)


def patch_zfs_snapshot(rel_path):
    return patch("zfs_snapshot.zfs_snapshot.%s" % (rel_path))


class TestArguments(unittest.TestCase):
    vdevs = ["bogus-vdev", "bogus-vdev/nested", "another/bogus/vdev"]

    def test_lifetime(self):
        parse_args(args=["--lifetime", "1"])
        parse_args(args=["--lifetime", "42"])
        with self.assertRaises(SystemExit):
            parse_args(args=["--lifetime", "-1"])
        with self.assertRaises(SystemExit):
            parse_args(args=["--lifetime", "apple"])

    def test_snapshot_period(self):
        for i, snapshot_category in enumerate(SNAPSHOT_CATEGORIES):
            name = snapshot_category.name
            opts = parse_args(args=["--snapshot-period", name])
            self.assertEquals(opts.snapshot_period, i)

            # Minor optimization: since here, we might as well test the default
            # case instead of trying to precompute the index out-of-band
            # somehow.
            if name == DEFAULT_SNAPSHOT_PERIOD:
                opts = parse_args(args=[])
                self.assertEquals(opts.snapshot_period, i)

        with self.assertRaises(SystemExit):
            parse_args(args=["--snapshot-period", "bogus"])

    def test_snapshot_prefix(self):
        opts = parse_args(args=[])
        self.assertEquals(opts.snapshot_prefix, DEFAULT_SNAPSHOT_PREFIX)
        opts = parse_args(args=["--snapshot-prefix", "bogus"])
        self.assertEquals(opts.snapshot_prefix, "bogus")
        with self.assertRaises(SystemExit):
            opts = parse_args(args=["--snapshot-prefix", ""])

    def test_vdev(self):
        vdevs = self.vdevs

        test_inputs_outputs_positive = [
            # __main__.main(..) will fill in the blanks later.
            [[], []],
            # Single option/argument pair.
            [["--vdev", vdevs[0]], [vdevs[0]]],
            # Multiple option/argument pair (accumulator).
            [["--vdev", vdevs[0], "--vdev", vdevs[-1]], [vdevs[0], vdevs[-1]]],
        ]
        test_inputs_outputs_negative = [
            ["--vdev", "doesnotexist"],
            ["--vdev", vdevs[0] + " "],
        ]

        with patch_zfs_snapshot("list_vdevs") as list_vdevs:
            list_vdevs.return_value = vdevs
            for args, test_output in test_inputs_outputs_positive:
                opts = parse_args(args=args)
                self.assertEquals(opts.vdevs, test_output)

            for args in test_inputs_outputs_negative:
                with self.assertRaises(SystemExit):
                    parse_args(args=args)


class TestMain(unittest.TestCase):
    def test_compute_cutoff(self):
        default_snapshot_type_index = period_type(DEFAULT_SNAPSHOT_PERIOD)
        default_snapshot_category = SNAPSHOT_CATEGORIES[default_snapshot_type_index]
        self.assertEquals(
            compute_cutoff(default_snapshot_category, 42),
            NOW - relativedelta(**{default_snapshot_category.name: 42}),
        )
        self.assertEquals(
            compute_cutoff(default_snapshot_category, None),
            NOW - default_snapshot_category.lifetime,
        )

    def test_compute_vdevs(self):
        all_vdevs = ["bogus-vdev", "bogus-vdev/nested", "another/bogus/vdev"]

        with patch_zfs_snapshot("list_vdevs") as list_vdevs, patch_zfs_snapshot(
            "zfs"
        ) as zfs:
            list_vdevs.return_value = all_vdevs

            zfs.side_effect = ["bogus-vdev\nbogus-vdev/nested\n"]
            # Recursive with --vdev
            self.assertEquals(
                compute_vdevs(["bogus-vdev"], True), ["bogus-vdev", "bogus-vdev/nested"]
            )
            zfs.assert_has_calls([call("list -H -o name -r %s" % ("bogus-vdev"))])
            zfs.reset_mock()

            # Recursive with --vdev, redux
            zfs.side_effect = [
                "bogus-vdev\nbogus-vdev/nested\n",
                "another/bogus/vdev\n",
            ]
            self.assertEquals(
                compute_vdevs(["bogus-vdev", "another/bogus/vdev"], True),
                ["bogus-vdev", "bogus-vdev/nested", "another/bogus/vdev"],
            )
            zfs.assert_has_calls(
                [
                    call("list -H -o name -r %s" % ("bogus-vdev")),
                    call("list -H -o name -r %s" % ("another/bogus/vdev")),
                ]
            )
            zfs.reset_mock()

            # Non-recursive with --vdev
            self.assertEquals(
                compute_vdevs(["bogus-vdev", "another/bogus/vdev"], False),
                ["bogus-vdev", "another/bogus/vdev"],
            )

            # Non-recursive with --vdev
            self.assertEquals(compute_vdevs(["bogus-vdev"], False), ["bogus-vdev"])

            # All vdevs
            self.assertEquals(compute_vdevs([], False), all_vdevs)
