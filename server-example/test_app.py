# Copyright 2020 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0
"Tests for app"

import pytest

import app


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


def test_image(client):
    rv = client.get("/img?left_text=build&right_text=passing")
    assert b'build' in rv.data
    assert b'passing' in rv.data
