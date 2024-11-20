# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Tests for PrecalculatedTextMeasurer."""

from pybadges2 import precalculated_text_measurer
import unittest


class TestPrecalculatedTextMeasurer(unittest.TestCase):

    def test_some_known_widths(self) -> None:
        measurer = precalculated_text_measurer.PrecalculatedTextMeasurer(
            default_character_width=5.1,
            char_to_width={
                'H': 1.2,
                'l': 1.3,
            },
            pair_to_kern={})

        text_width = measurer.text_width('Hello')
        self.assertAlmostEqual(text_width, 1.2 + 5.1 + 1.3 + 1.3 + 5.1)

    def test_kern_in_middle(self) -> None:
        measurer = precalculated_text_measurer.PrecalculatedTextMeasurer(
            default_character_width=5,
            char_to_width={},
            pair_to_kern={
                'el': 3.3,
                'll': 4.4,
                'no': 5.5,
            })

        text_width = measurer.text_width('Hello')
        self.assertAlmostEqual(text_width, 5 * 5 - 3.3 - 4.4)

    def test_kern_at_start(self) -> None:
        measurer = precalculated_text_measurer.PrecalculatedTextMeasurer(
            default_character_width=5,
            char_to_width={},
            pair_to_kern={
                'He': 3.3,
                'no': 4.4,
            })

        text_width = measurer.text_width('Hello')
        self.assertAlmostEqual(text_width, 5 * 5 - 3.3)

    def test_kern_at_end(self) -> None:
        measurer = precalculated_text_measurer.PrecalculatedTextMeasurer(
            default_character_width=5,
            char_to_width={},
            pair_to_kern={
                'lo': 3.3,
                'no': 4.4,
            })

        text_width = measurer.text_width('Hello')
        self.assertAlmostEqual(text_width, 5 * 5 - 3.3)

    def test_default_usable(self) -> None:
        measurer = (
            precalculated_text_measurer.PrecalculatedTextMeasurer.default())
        measurer.text_width('This is a long string of text')


if __name__ == '__main__':
    unittest.main()
