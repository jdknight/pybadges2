# Copyright 2018 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0
"""Measure the width, in pixels, of a string rendered using DejaVu Sans 110pt.

Uses a PIL/Pillow to determine the string length.
"""

from PIL import ImageFont

from pybadges2 import text_measurer


class PilMeasurer(text_measurer.TextMeasurer):
    """Measures the width of a string using PIL/Pillow."""

    def __init__(self, deja_vu_sans_path: str):
        """Initializer for PilMeasurer.

        Args:
            deja_vu_sans_path: The path to the DejaVu Sans TrueType (.ttf) font
                file.
        """
        self._font = ImageFont.truetype(deja_vu_sans_path, 110)

    def text_width(self, text: str) -> float:
        """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
        width, _ = self._font.getsize(text)
        return width
