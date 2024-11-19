# Copyright 2022 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0
"""An HTTP image server that can be used to set logo embedding.

The server will respond to any request with the image data provided in the
constructor.
"""

from http import server
import threading


class ImageServer:

    def __init__(self, image_data):
        self._image_data = image_data

    def start_server(self):
        srv = self

        class Handler(server.BaseHTTPRequestHandler):

            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                self.wfile.write(srv._image_data)

        self._httpd = server.HTTPServer(('localhost', 0), Handler)
        self.logo_url = "http://localhost:{0}".format(self._httpd.server_port)

        thread = threading.Thread(target=self._httpd.serve_forever)
        thread.start()

    def fix_embedded_url_reference(self, example):
        if example.get("logo") == "<embedded>":
            example["logo"] = self.logo_url

    def stop_server(self):
        self._httpd.shutdown()