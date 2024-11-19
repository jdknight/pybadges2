#!/usr/bin/env python3
# Copyright 2018 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
import os.path
import pkg_resources

import pybadges2
from tests import image_server
from tests import test_pybadges


def generate_images(source_json_path, target_directory):
    srv = image_server.ImageServer(test_pybadges.PNG_IMAGE)
    srv.start_server()
    try:
        os.makedirs(target_directory, exist_ok=True)
        with open(source_json_path) as f:
            examples = json.load(f)

        for example in examples:
            srv.fix_embedded_url_reference(example)
            filename = os.path.join(target_directory, example.pop('file_name'))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(pybadges.badge(**example))
    finally:
        srv.stop_server()


def main():
    parser = argparse.ArgumentParser(
        description='generate a github-style badge given some text and colors')

    parser.add_argument(
        '--source-path',
        default=pkg_resources.resource_filename(__name__,
                                                'tests/test-badges.json'),
        help='the text to show on the left-hand-side of the badge')

    parser.add_argument(
        '--destination-dir',
        default=pkg_resources.resource_filename(__name__,
                                                'tests/golden-images'),
        help='the text to show on the left-hand-side of the badge')
    args = parser.parse_args()
    generate_images(args.source_path, args.destination_dir)


if __name__ == '__main__':
    main()
