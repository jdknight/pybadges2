# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
"""Output a github-style badge as an SVG image given some text and colors.

For more information, run:
$ python3 -m pybadges2 --help
"""

from pathlib import Path
from pybadges2 import badge
from pybadges2 import pil_text_measurer
from pybadges2.version import __version__
import argparse
import sys
import tempfile
import webbrowser


def main() -> None:
    parser = argparse.ArgumentParser(
        'pybadges2',
        description='generate a github-style badge given some text and colors')

    parser.add_argument(
        '--left-text',
        default='license',
        help='the text to show on the left-hand-side of the badge')
    parser.add_argument(
        '--right-text',
        default=None,
        help='the text to show on the right-hand-side of the badge')
    parser.add_argument(
        '--left-link',
        default=None,
        help='the url to redirect to when the left-hand of the badge is '
        'clicked')
    parser.add_argument(
        '--right-link',
        default=None,
        help='the url to redirect to when the right-hand of the badge is '
        'clicked')
    parser.add_argument(
        '--center-link',
        default=None,
        help='the url to redirect to when the center of the badge is '
        'clicked')
    parser.add_argument('--whole-link',
                        default=None,
                        help='the url to redirect to when the badge is clicked')
    parser.add_argument(
        '--logo',
        default=None,
        help='a URI reference to a logo to display in the badge')
    parser.add_argument(
        '--left-color',
        default='#555',
        help='the background color of the left-hand-side of the badge')
    parser.add_argument(
        '--right-color',
        default='#007ec6',
        help='the background color of the right-hand-side of the badge')
    parser.add_argument(
        '--center-color',
        default=None,
        help='the background color of the right-hand-side of the badge')
    parser.add_argument('--browser',
                        action='store_true',
                        default=False,
                        help='display the badge in a browser tab')
    parser.add_argument(
        '--use-pil-text-measurer',
        action='store_true',
        default=False,
        help='use the PilMeasurer to measure the length of text (kerning may '
        'be more precise for non-Western languages. '
        '--deja-vu-sans-path must also be set.')
    parser.add_argument(
        '--deja-vu-sans-path',
        default=None,
        help='the path to the ttf font file containing DejaVu Sans. If not '
        'present on your system, you can download it from '
        'https://www.fontsquirrel.com/fonts/dejavu-sans')
    parser.add_argument(
        '--left-title',
        default=None,
        help='the title to associate with the left part of the badge. See '
        'https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title')
    parser.add_argument(
        '--right-title',
        default=None,
        help='the title to associate with the right part of the badge. See '
        'https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title')
    parser.add_argument(
        '--center-title',
        default=None,
        help='the title to associate with the center part of the badge. See '
        'https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title')
    parser.add_argument(
        '--whole-title',
        default=None,
        help='the title to associate with the entire badge. See '
        'https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title')
    parser.add_argument(
        '--right-image',
        default=None,
        help='the image to associate with the right-hand side of the badge')
    parser.add_argument(
        '--center-image',
        default=None,
        help='the image to associate with the center of the badge')
    parser.add_argument(
        '--embed-logo',
        nargs='?',
        type=lambda x: x.lower() in ['y', 'yes', 't', 'true', '1', ''],
        const='yes',
        default='no',
        help='if the logo is specified then include the image data directly in '
        'the badge (this will prevent a URL fetch and may work around the '
        'fact that some browsers do not fetch external image references); '
        'only works if --logo is a HTTP/HTTPS URI or a file path')
    parser.add_argument(
        '--embed-timeout',
        nargs='?',
        type=int,
        help='if the logo is specified then this value will be used to '
        'control the timeout of a URL fetch')
    parser.add_argument(
        '--embed-right-image',
        nargs='?',
        type=lambda x: x.lower() in ['y', 'yes', 't', 'true', '1', ''],
        const='yes',
        default='no',
        help=
        'if the right image is specified then include the image data directly in '
        'the badge (this will prevent a URL fetch and may work around the '
        'fact that some browsers do not fetch external image references); '
        'only works if --logo is a HTTP/HTTPS URI or a file path')
    parser.add_argument(
        '--embed-center-image',
        nargs='?',
        type=lambda x: x.lower() in ['y', 'yes', 't', 'true', '1', ''],
        const='yes',
        default='no',
        help=
        'if the center image is specified then include the image data directly in '
        'the badge (this will prevent a URL fetch and may work around the '
        'fact that some browsers do not fetch external image references); '
        'only works if --logo is a HTTP/HTTPS URI or a file path')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    if (args.left_link or args.right_link or
            args.center_link) and args.whole_link:
        print('argument --whole-link: cannot be set with '
              '--left-link, --right-link, or --center_link',
              file=sys.stderr)
        sys.exit(1)

    measurer = None
    if args.use_pil_text_measurer:
        if args.deja_vu_sans_path is None:
            print('argument --use-pil-text-measurer: must also set '
                  '--deja-vu-sans-path',
                  file=sys.stderr)
            sys.exit(1)
        measurer = pil_text_measurer.PilMeasurer(args.deja_vu_sans_path)

    generated_badge = badge(
        left_text=args.left_text,
        right_text=args.right_text,
        left_link=args.left_link,
        right_link=args.right_link,
        center_link=args.center_link,
        whole_link=args.whole_link,
        logo=args.logo,
        left_color=args.left_color,
        right_color=args.right_color,
        center_color=args.center_color,
        measurer=measurer,
        left_title=args.left_title,
        right_title=args.right_title,
        center_title=args.center_title,
        whole_title=args.whole_title,
        right_image=args.right_image,
        center_image=args.center_image,
        embed_logo=args.embed_logo,
        embed_timeout=args.embed_timeout,
        embed_right_image=args.embed_right_image,
        embed_center_image=args.embed_center_image,
    )

    if args.browser:
        _, badge_path = tempfile.mkstemp(suffix='.svg')
        with Path(badge_path).open('w') as f:
            f.write(generated_badge)

        webbrowser.open_new_tab('file://' + badge_path)
    else:
        print(generated_badge, end='')


main()
