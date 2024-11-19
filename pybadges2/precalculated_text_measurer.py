# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Measure the width, in pixels, of a string rendered using DejaVu Sans 110pt.

Uses a precalculated set of metrics to calculate the string length.
"""

from pathlib import Path
from pybadges2 import text_measurer
from typing import Mapping
from typing import TextIO
import json
import lzma


class PrecalculatedTextMeasurer(text_measurer.TextMeasurer):
    """Measures the width of a string using a precalculated set of tables."""

    _default_cache = None

    def __init__(self, default_character_width: float,
                 char_to_width: Mapping[str, float],
                 pair_to_kern: Mapping[str, float]) -> None:
        """Initializer for PrecalculatedTextMeasurer.

        Args:
            default_character_width: the average width, in pixels, of a
                character in DejaVu Sans 110pt.
            char_to_width: a mapping between a character and it's width,
                in pixels, in DejaVu Sans 110pt.
            pair_to_kern: a mapping between pairs of characters and the kerning
                distance between them e.g. text_width("IJ") =>
                    (char_to_width["I"] + char_to_width["J"]
                    - pair_to_kern.get("IJ", 0))
        """
        self._default_character_width = default_character_width
        self._char_to_width = char_to_width
        self._pair_to_kern = pair_to_kern

    def text_width(self, text: str) -> float:
        """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
        width = 0
        for index, c in enumerate(text):
            width += self._char_to_width.get(c, self._default_character_width)
            width -= self._pair_to_kern.get(text[index:index + 2], 0)

        return width

    @staticmethod
    def from_json(f: TextIO) -> 'PrecalculatedTextMeasurer':
        """Return a PrecalculatedTextMeasurer given a JSON stream.

        See precalculate_text.py for details on the required format.
        """
        o = json.load(f)
        return PrecalculatedTextMeasurer(o['mean-character-length'],
                                         o['character-lengths'],
                                         o['kerning-pairs'])

    @classmethod
    def default(cls) -> 'PrecalculatedTextMeasurer':
        """Returns a reasonable default PrecalculatedTextMeasurer."""
        if cls._default_cache is not None:
            return cls._default_cache

        module_dir = Path(__file__).parent

        default_widths_xz = module_dir / 'default-widths.json.xz'
        if default_widths_xz.is_file():
            with default_widths_xz.open('rb') as f, lzma.open(f, 'rt') as g:
                cls._default_cache = PrecalculatedTextMeasurer.from_json(g)
                return cls._default_cache
        else:
            default_widths = module_dir / 'default-widths.json'
            with default_widths.open(encoding='utf-8') as f:
                cls._default_cache = PrecalculatedTextMeasurer.from_json(f)
                return cls._default_cache
