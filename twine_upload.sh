#!/usr/bin/env bash
# Copyright 2019 The pybadge Authors
# SPDX-License-Identifier: Apache-2.0

set -ev

# If this is not a CircleCI tag, no-op.
if [[ -z "$CIRCLE_TAG" ]]; then
  echo "This is not a release tag. Doing nothing."
  exit 0
fi

# Build the distribution and upload.
python3 setup.py sdist bdist_wheel
twine upload dist/* --username $PYPI_USERNAME --password $PYPI_PASSWORD
