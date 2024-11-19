# Copyright 2023 by the Sphinx team (sphinx-doc/sphinx). All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations


def detect_image_type(data: bytes) -> str | None:
    # Bitmap
    # https://wikipedia.org/wiki/BMP_file_format#Bitmap_file_header
    if data.startswith(b'BM'):
        return 'bmp'

    # GIF
    # https://wikipedia.org/wiki/GIF#File_format
    if data.startswith((b'GIF87a', b'GIF89a')):
        return 'gif'

    # JPEG data
    # https://wikipedia.org/wiki/JPEG_File_Interchange_Format#File_format_structure
    if data.startswith(b'\xFF\xD8'):
        return 'jpeg'

    # Portable Network Graphics
    # https://wikipedia.org/wiki/PNG#File_header
    if data.startswith(b'\x89PNG\r\n\x1A\n'):
        return 'png'

    # Scalable Vector Graphics
    # https://svgwg.org/svg2-draft/struct.html
    if b'<svg' in data.lower():
        return 'svg+xml'

    # TIFF
    # https://wikipedia.org/wiki/TIFF#Byte_order
    if data.startswith((b'MM', b'II')):
        return 'tiff'

    # WebP
    # https://wikipedia.org/wiki/WebP#Technology
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'webp'

    return None
