# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
#
# Use the same color scheme as describe in:
# https://github.com/badges/shields/blob/5cdef88bcc65da9dbb1f85f7e987f1148c4ae757/badge-maker/lib/color.js#L6

from xml.dom import minidom


_NAME_TO_COLOR = {
    'brightgreen': '#4c1',
    'green': '#97CA00',
    'yellow': '#dfb317',
    'yellowgreen': '#a4a61d',
    'orange': '#fe7d37',
    'red': '#e05d44',
    'blue': '#007ec6',
    'grey': '#555',
    'gray': '#555',
    'lightgrey': '#9f9f9f',
    'lightgray': '#9f9f9f',
    'critical': '#e05d44',
    'important': '#fe7d37',
    'success': '#4c1',
    'informational': '#007ec6',
    'inactive': '#9f9f9f',
}


def name2color(color: str) -> str:
    return _NAME_TO_COLOR.get(color, color)


def remove_xml_blanks(node: minidom.Node) -> None:
    for x in node.childNodes:
        if x.nodeType == minidom.Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == minidom.Node.ELEMENT_NODE:
            remove_xml_blanks(x)
