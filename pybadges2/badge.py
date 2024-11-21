# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Creates a github-style badge as a SVG image.

This package seeks to generate semantically-identical output to the JavaScript
gh-badges library
(https://github.com/badges/shields/blob/master/doc/gh-badges.md)

>>> badge(left_text='coverage', right_text='23%', right_color='red')
'<svg...</svg>'
>>> badge(left_text='build', right_text='green', right_color='green',
...       whole_link="http://www.example.com/")
'<svg...</svg>'
>>> # base64-encoded PNG image
>>> image_data = (
>>>     'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zw'
>>>     'AD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC'
>>> )
>>> badge(left_text='build', right_text='green', right_color='green',
...       logo="data:image/png;base64," + image_data)
'<svg...</svg>'
"""

from __future__ import annotations
from pybadges2 import precalculated_text_measurer
from pybadges2 import text_measurer
from pybadges2.embed_image import embed_image
from pybadges2.util import name2color
from pybadges2.util import remove_xml_blanks
from xml.dom import minidom
import jinja2

_JINJA2_ENVIRONMENT = jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=jinja2.PackageLoader('pybadges2', '.'),
    autoescape=jinja2.select_autoescape(['svg']))


def badge(
    left_text: str,
    *,
    right_text: str | None = None,
    left_link: str | None = None,
    right_link: str | None = None,
    center_link: str | None = None,
    whole_link: str | None = None,
    logo: str | None = None,
    left_color: str = '#555',
    right_color: str = '#007ec6',
    center_color: str | None = None,
    measurer: text_measurer.TextMeasurer | None = None,
    left_title: str | None = None,
    right_title: str | None = None,
    center_title: str | None = None,
    whole_title: str | None = None,
    right_image: str | None = None,
    center_image: str | None = None,
    embed_logo: bool = False,
    embed_timeout: int | None = None,
    embed_right_image: bool = False,
    embed_center_image: bool = False,
    id_suffix: str = '',
) -> str:
    """Creates a github-style badge as an SVG image.

    >>> badge(left_text='coverage', right_text='23%', right_color='red')
    '<svg...</svg>'
    >>> badge(left_text='build', right_text='green', right_color='green',
    ...       whole_link="http://www.example.com/")
    '<svg...</svg>'

    Args:
        left_text: The text that should appear on the left-hand-side of the
            badge e.g. "coverage".
        right_text: The text that should appear on the right-hand-side of the
            badge e.g. "23%".
        left_link: The URL that should be redirected to when the left-hand text
            is selected.
        right_link: The URL that should be redirected to when the right-hand
            text is selected.
        whole_link: The link that should be redirected to when the badge is
            selected. If set then left_link and right_right may not be set.
        logo: A url representing a logo that will be displayed inside the
            badge. Can be a data URL e.g. "data:image/svg+xml;utf8,<svg..."
        left_color: The color of the part of the badge containing the left-hand
            text. Can be an valid CSS color
            (see https://developer.mozilla.org/en-US/docs/Web/CSS/color) or a
            color name defined here:
            https://github.com/badges/shields/blob/master/badge-maker/lib/color.js
        right_color: The color of the part of the badge containing the
            right-hand text. Can be an valid CSS color
            (see https://developer.mozilla.org/en-US/docs/Web/CSS/color) or a
            color name defined here:
            https://github.com/badges/shields/blob/master/badge-maker/lib/color.js
        measurer: A text_measurer.TextMeasurer that can be used to measure the
            width of left_text and right_text.
        embed_logo: If True then embed the logo image directly in the badge.
            This can prevent an HTTP request and some browsers will not render
            external image referenced. When True, `logo` must be a HTTP/HTTPS
            URI or a filesystem path. Also, the `badge` call may raise an
            exception if the logo cannot be loaded, is not an image, etc.
        embed_timeout: Timeout for any request to fetch logo to embed.
        whole_title: The title attribute to associate with the entire badge.
            See https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title.
        left_title: The title attribute to associate with the left part of the
            badge.
            See https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title.
        right_title: The title attribute to associate with the right part of
            the badge.
            See https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title.
        id_suffix: The suffix of the id attributes used in the SVG's elements.
            Use to prevent duplicate ids if several badges are embedded on the
            same page.
    """
    if measurer is None:
        measurer = (
            precalculated_text_measurer.PrecalculatedTextMeasurer.default())

    if (left_link or right_link or center_link) and whole_link:
        msg = 'whole_link may not bet set with left_link, right_link, or center_link'
        raise ValueError(msg)

    if center_image and not (right_image or right_text):
        msg = 'cannot have a center_image without a right element'
        raise ValueError(msg)

    if (center_image and not center_color) or (not center_image and
                                               center_color):
        msg = 'must have both a center_image and a center_color'
        raise ValueError(msg)

    if logo and embed_logo:
        logo = embed_image(logo, http_timeout=embed_timeout)

    if right_image and embed_right_image:
        right_image = embed_image(right_image, http_timeout=embed_timeout)

    if center_image and embed_center_image:
        center_image = embed_image(center_image, http_timeout=embed_timeout)

    if center_color:
        center_color = name2color(center_color)

    right_text_width = None
    if right_text:
        right_text_width = measurer.text_width(right_text) / 10.0

    template = _JINJA2_ENVIRONMENT.get_template('badge-template-full.svg')

    svg = template.render(
        left_text=left_text,
        right_text=right_text,
        left_text_width=measurer.text_width(left_text) / 10.0,
        right_text_width=right_text_width,
        left_link=left_link,
        right_link=right_link,
        whole_link=whole_link,
        center_link=center_link,
        logo=logo,
        left_color=name2color(left_color),
        right_color=name2color(right_color),
        center_color=center_color,
        left_title=left_title,
        right_title=right_title,
        center_title=center_title,
        whole_title=whole_title,
        right_image=right_image,
        center_image=center_image,
        id_suffix=id_suffix,
    )
    xml = minidom.parseString(svg)  # noqa: S318
    remove_xml_blanks(xml)
    xml.normalize()
    return xml.documentElement.toxml()
