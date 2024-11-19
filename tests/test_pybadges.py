# Copyright 2018 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0
"""Tests for pybadges2."""

from pathlib import Path
from tests import image_server
import base64
import doctest
import json
import os.path
import pathlib
import pybadges2
import sys
import tempfile
import unittest
import xmldiff.main

TEST_DIR = os.path.dirname(__file__)

PNG_IMAGE_B64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zw'
    'AD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC')
PNG_IMAGE = base64.b64decode(PNG_IMAGE_B64)


class TestPybadges2Badge(unittest.TestCase):
    """Tests for pybadges2.badge."""

    def setUp(self):
        super().setUp()
        self._image_server = image_server.ImageServer(PNG_IMAGE)
        self._image_server.start_server()

    def tearDown(self):
        super().tearDown()
        self._image_server.stop_server()

    def test_docs(self):
        doctest.testmod(pybadges2, optionflags=doctest.ELLIPSIS)

    def test_whole_link_and_left_link(self):
        with self.assertRaises(ValueError):
            pybadges2.badge(left_text='foo',
                           right_text='bar',
                           left_link='http://example.com/',
                           whole_link='http://example.com/')

    def test_changes(self):
        with open(os.path.join(TEST_DIR, 'test-badges.json'), 'r') as f:
            examples = json.load(f)

        for example in examples:
            self._image_server.fix_embedded_url_reference(example)
            file_name = example.pop('file_name')
            with self.subTest(example=file_name):
                goldenpath = os.path.join(TEST_DIR, 'golden-images', file_name)

                with open(goldenpath, mode="r", encoding="utf-8") as f:
                    golden_image = f.read()
                pybadge_image = pybadges2.badge(**example)

                diff = xmldiff.main.diff_texts(golden_image, pybadge_image)
                if diff:
                    with tempfile.NamedTemporaryFile(mode="w+t",
                                                     encoding="utf-8",
                                                     delete=False,
                                                     suffix=".svg") as actual:
                        actual.write(pybadge_image)

                    with tempfile.NamedTemporaryFile(mode="w+t",
                                                     delete=False,
                                                     suffix=".html") as html:
                        html.write("""
                        <html>
                            <body>
                                <img src="file://%s"><br>
                                <img src="file://%s">
                            <body>
                        </html>""" % (goldenpath, actual.name))
                    self.fail(
                        "images for %s differ:\n%s\nview with:\npython -m webbrowser %s"
                        % (file_name, diff, html.name))


class TestEmbedImage(unittest.TestCase):
    """Tests for pybadges2._embed_image."""

    def test_data_url(self):
        url = 'data:image/png;base64,' + PNG_IMAGE_B64
        self.assertEqual(url, pybadges2._embed_image(url))

    def test_http_url(self):
        url = 'https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg'
        self.assertRegex(pybadges2._embed_image(url),
                         r'^data:image/svg(\+xml)?;base64,')

    def test_not_image_url(self):
        with self.assertRaisesRegex(ValueError,
                                    'expected an image, got "text"'):
            pybadges2._embed_image('http://www.google.com/')

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix filesystem")
    def test_svg_file_path(self):
        image_path = os.path.abspath(
            os.path.join(TEST_DIR, 'golden-images', 'build-failure.svg'))
        self.assertRegex(pybadges2._embed_image(image_path),
                         r'^data:image/svg(\+xml)?;base64,')

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix filesystem")
    def test_png_file_path(self):
        with tempfile.NamedTemporaryFile() as png:
            png.write(PNG_IMAGE)
            png.flush()
            self.assertEqual(pybadges2._embed_image(png.name),
                             'data:image/png;base64,' + PNG_IMAGE_B64)

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix filesystem")
    def test_unknown_type_file_path(self):
        with tempfile.NamedTemporaryFile() as non_image:
            non_image.write(b'Hello')
            non_image.flush()
            with self.assertRaisesRegex(ValueError,
                                        'not able to determine file type'):
                pybadges2._embed_image(non_image.name)

    @unittest.skipIf(sys.platform.startswith("win"), "requires Unix filesystem")
    def test_text_file_path(self):
        with tempfile.NamedTemporaryFile(suffix='.txt') as non_image:
            non_image.write(b'Hello')
            non_image.flush()
            with self.assertRaisesRegex(ValueError,
                                        'expected an image, got "text"'):
                pybadges2._embed_image(non_image.name)

    def test_file_url(self):
        image_path = os.path.abspath(
            os.path.join(TEST_DIR, 'golden-images', 'build-failure.svg'))

        with self.assertRaisesRegex(ValueError, 'unsupported scheme "file"'):
            pybadges2._embed_image(pathlib.Path(image_path).as_uri())


if __name__ == '__main__':
    unittest.main()
