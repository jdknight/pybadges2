# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from tests import image_server
from tests import test_pybadges
import argparse
import json
import pybadges2


def generate_images(source_json_path: Path, target_directory: Path) -> None:
    srv = image_server.ImageServer(test_pybadges.PNG_IMAGE)
    srv.start_server()
    try:
        target_directory.mkdir(parents=True, exist_ok=True)
        with source_json_path.open() as f:
            examples = json.load(f)

        for example in examples:
            srv.fix_embedded_url_reference(example)
            filename = target_directory / example.pop('file_name')
            with filename.open('w', encoding='utf-8') as f:
                f.write(pybadges2.badge(**example))
    finally:
        srv.stop_server()


def main() -> None:
    root_dir = Path(__file__).parent.parent.parent
    test_assets_dir = root_dir / 'tests' / 'assets'

    parser = argparse.ArgumentParser(
        description='generate a github-style badge given some text and colors')

    parser.add_argument(
        '--source-path',
        default=test_assets_dir / 'test-badges.json',
        help='the text to show on the left-hand-side of the badge')

    parser.add_argument(
        '--destination-dir',
        default=test_assets_dir / 'golden-images',
        help='the text to show on the left-hand-side of the badge')
    args = parser.parse_args()
    generate_images(args.source_path, args.destination_dir)


if __name__ == '__main__':
    main()
