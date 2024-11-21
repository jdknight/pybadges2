# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Tests for pybadges2."""

from __future__ import annotations
from pathlib import Path
from pybadges2.embed_image import embed_image
from tests import image_server
import base64
import doctest
import json
import pybadges2
import sys
import tempfile
import unittest
import xmldiff.main

PNG_IMAGE_B64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zw'
    'AD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC')
PNG_IMAGE = base64.b64decode(PNG_IMAGE_B64)


class TestPybadges2Badge(unittest.TestCase):
    """Tests for pybadges2.badge."""

    @classmethod
    def setUpClass(cls: type[unittest.TestCase]) -> None:
        test_dir = Path(__file__).parent
        cls.dataset = test_dir / 'assets'

    def setUp(self) -> None:
        super().setUp()
        self._image_server = image_server.ImageServer(PNG_IMAGE)
        self._image_server.start_server()

    def tearDown(self) -> None:
        super().tearDown()
        self._image_server.stop_server()

    def test_docs(self) -> None:
        doctest.testmod(pybadges2, optionflags=doctest.ELLIPSIS)

    def test_whole_link_and_left_link(self) -> None:
        with self.assertRaises(ValueError):
            pybadges2.badge(left_text='foo',
                           right_text='bar',
                           left_link='http://example.com/',
                           whole_link='http://example.com/')

    def test_changes(self) -> None:
        test_badges = self.dataset / 'test-badges.json'

        with test_badges.open() as f:
            examples = json.load(f)

        for example in examples:
            self._image_server.fix_embedded_url_reference(example)
            file_name = example.pop('file_name')
            with self.subTest(example=file_name):
                example_img = self.dataset / 'golden-images' / file_name

                with example_img.open(encoding='utf-8') as f:
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
                        html.write(f"""
                        <html>
                            <body>
                                <img src="file://{example_img}"><br>
                                <img src="file://{actual.name}">
                            <body>
                        </html>""")
                    self.fail(
                        'images for {file_name} differ:\n{diff}\n'
                        'view with:\npython -m webbrowser {html.name}',
                    )


class TestEmbedImage(unittest.TestCase):
    """Tests for embed_image."""

    @classmethod
    def setUpClass(cls: type[unittest.TestCase]) -> None:
        test_dir = Path(__file__).parent
        cls.dataset = test_dir / 'assets'

    def test_data_url(self) -> None:
        url = 'data:image/png;base64,' + PNG_IMAGE_B64
        self.assertEqual(url, embed_image(url))

    def test_http_url(self) -> None:
        url = 'https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg'
        self.assertRegex(embed_image(url),
                         r'^data:image/svg(\+xml)?;base64,')

    def test_not_image_url(self) -> None:
        with self.assertRaisesRegex(ValueError,
                                    'expected an image, got "text"'):
            embed_image('http://www.google.com/')

    def test_svg_file_path(self) -> None:
        image_path = self.dataset / 'golden-images' / 'build-failure.svg'
        self.assertRegex(embed_image(image_path),
                         r'^data:image/svg(\+xml)?;base64,')

    def test_png_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as work_dir:
            tmpfile = Path(work_dir) / 'test.png'
            with tmpfile.open('wb') as f:
                f.write(PNG_IMAGE)

            self.assertEqual(embed_image(tmpfile),
                             'data:image/png;base64,' + PNG_IMAGE_B64)

    def test_unknown_type_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as work_dir:
            tmpfile = Path(work_dir) / 'unknown'
            with tmpfile.open('wb') as f:
                f.write(b'Hello')

            with self.assertRaisesRegex(ValueError,
                                        'not able to determine file type'):
                embed_image(tmpfile)

    def test_text_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as work_dir:
            tmpfile = Path(work_dir) / 'test.txt'
            with tmpfile.open('wb') as f:
                f.write(b'Hello')

            with self.assertRaisesRegex(ValueError,
                                        'expected an image, got "text"'):
                embed_image(tmpfile)

    @unittest.skipIf(sys.version_info<(3, 13, 0), 'requires python v3.13+')
    def test_file_url(self) -> None:
        image_path = self.dataset / 'golden-images' / 'build-failure.svg'
        self.assertRegex(embed_image(Path(image_path).as_uri()),
                         r'^data:image/svg(\+xml)?;base64,')


if __name__ == '__main__':
    unittest.main()
