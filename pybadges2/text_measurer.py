# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Measure the width, in pixels, of a  string rendered using DejaVu Sans 110pt.

Contains only an abstract base class.
"""


class TextMeasurer:
    """The abstract base class for text measuring classes."""

    def text_width(self, text: str) -> float:
        """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
        msg = 'text_width not implemented'
        raise NotImplementedError(msg)
