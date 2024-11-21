# Copyright 2018 The pybadge Authors
# Copyright pybadge2 Authors
# SPDX-License-Identifier: Apache-2.0
#
# Use the same color scheme as describe in:
# https://github.com/badges/shields/blob/5cdef88bcc65da9dbb1f85f7e987f1148c4ae757/badge-maker/lib/color.js#L6

from __future__ import annotations
from pathlib import Path
from pybadges2.detect_image_type import detect_image_type
import base64
import mimetypes
import requests
import urllib.parse

# default timeout (in seconds)
DEFAULT_TIMEOUT = 10


def embed_image(content: str | Path, http_timeout: int | None = None) -> str:
    if isinstance(content, str):
        parsed_url = urllib.parse.urlparse(content)

        # raw data; use the provided data
        if parsed_url.scheme == 'data':
            return content

        if parsed_url.scheme == 'file':
            try:
                src_path = Path.from_uri(content)
            except AttributeError as ex:
                msg = 'file uri not supported (pre-Python v3.13)'
                raise ValueError(msg) from ex
            image_type, image_data = embed_image_from_file(src_path)
        elif parsed_url.scheme.startswith('http'):
            image_type, image_data = \
                embed_image_from_url(content, timeout=http_timeout)
        else:
            src_path = Path(content)
            if src_path.is_file():
                image_type, image_data = embed_image_from_file(src_path)
            else:
                msg = f'unsupported scheme "{parsed_url.scheme}"'
                raise ValueError(msg)
    else:
        image_type, image_data = embed_image_from_file(content)

    encoded_image = base64.b64encode(image_data).decode('ascii')
    return f'data:image/{image_type};base64,{encoded_image}'


def embed_image_from_url(url: str, timeout: int | None = None) -> str:
    to = timeout if timeout else DEFAULT_TIMEOUT
    r = requests.get(url, timeout=to)
    r.raise_for_status()

    content_type = r.headers.get('content-type')
    if content_type is None:
        msg = 'no "Content-Type" header'
        raise ValueError(msg)

    content_type, image_type = content_type.split('/')
    if content_type != 'image':
        msg = f'expected an image, got "{content_type}"'
        raise ValueError(msg)

    return image_type, r.content


def embed_image_from_file(path: Path) -> str:
    with path.open('rb') as f:
        image_data = f.read()

    image_type = detect_image_type(image_data)
    if not image_type:
        mime_type, _ = mimetypes.guess_type(path, strict=False)
        if not mime_type:
            msg = 'not able to determine file type'
            raise ValueError(msg)

        content_type, image_type = mime_type.split('/')
        if content_type != 'image':
            desc = content_type or 'unknown'
            msg = f'expected an image, got "{desc}"'
            raise ValueError(msg)

    return image_type, image_data
