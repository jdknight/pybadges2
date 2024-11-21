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


def embed_image(url: str, http_timeout: int | None = None) -> str:
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme == 'data':
        return url

    if parsed_url.scheme.startswith('http'):
        timeout = http_timeout if http_timeout else DEFAULT_TIMEOUT
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        content_type = r.headers.get('content-type')
        if content_type is None:
            msg = 'no "Content-Type" header'
            raise ValueError(msg)
        content_type, image_type = content_type.split('/')
        if content_type != 'image':
            msg = f'expected an image, got "{content_type}"'
            raise ValueError(msg)
        image_data = r.content
    elif parsed_url.scheme:
        msg = f'unsupported scheme "{parsed_url.scheme}"'
        raise ValueError(msg)
    else:
        with Path(url).open('rb') as f:
            image_data = f.read()
        image_type = detect_image_type(image_data)
        if not image_type:
            mime_type, _ = mimetypes.guess_type(url, strict=False)
            if not mime_type:
                msg = 'not able to determine file type'
                raise ValueError(msg)

            content_type, image_type = mime_type.split('/')
            if content_type != 'image':
                desc = content_type or 'unknown'
                msg = f'expected an image, got "{desc}"'
                raise ValueError(msg)

    encoded_image = base64.b64encode(image_data).decode('ascii')
    return f'data:image/{image_type};base64,{encoded_image}'
