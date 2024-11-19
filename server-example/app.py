# Copyright 2020 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0
""" Example Flask server that serves badges."""

import flask
import pybadges2

app = flask.Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """Serve an HTML page containing badge images."""
    badges = [
        {
            'left_text': 'Build',
            'right_text': 'passing',
            'left_color': '#555',
            'right_color': '#008000'
        },
        {
            'left_text': 'Build',
            'right_text': 'fail',
            'left_color': '#555',
            'right_color': '#800000'
        },
        {
            "left_text":
                "complete",
            "right_text":
                "example",
            "left_color":
                "green",
            "right_color":
                "yellow",
            "logo":
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zwAD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC"
        },
    ]
    for b in badges:
        b['url'] = flask.url_for('.serve_badge', **b)
    return flask.render_template('index.html', badges=badges)


@app.route('/img')
def serve_badge():
    """Serve a badge image based on the request query string."""
    badge = pybadges2.badge(left_text=flask.request.args.get('left_text'),
                           right_text=flask.request.args.get('right_text'),
                           left_color=flask.request.args.get('left_color'),
                           right_color=flask.request.args.get('right_color'),
                           logo=flask.request.args.get('logo'))

    response = flask.make_response(badge)
    response.content_type = 'image/svg+xml'
    return response


if __name__ == '__main__':
    app.run()
