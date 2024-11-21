[![pip Version](https://badgen.net/pypi/v/pybadges2?label=PyPI)](https://pypi.python.org/pypi/pybadges2)
[![Supports Various Python versions](https://badgen.net/pypi/python/pybadges2?label=Python)](https://pypi.python.org/pypi/pybadges2)
[![Build Status](https://github.com/jdknight/pybadges2/actions/workflows/build.yml/badge.svg)](https://github.com/jdknight/pybadges2/actions/workflows/build.yml)

# pybadges2

> [!IMPORTANT]
> The pybadges2 is a new release (end of 2024) based on the original
> [pybadges][pybadges] repository. The primary goal is to support the
> maintenace of this library/utility (since upstream maintenance appears
> to have paused).

pybadges2 is a Python library and command line tool that allows you to create
Github-style badges as SVG images. For example:

<p align="center">
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/pip.svg" />
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/license.svg" />
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/build-passing.svg" />
</p>

The aesthetics of the generated badges matches the visual design found in this
[specification][badges-shields-spec].

The implementation of the library was heavily influenced by
[Shields.io][shields-io] and the JavaScript [badge-maker][badge-maker] library.

## Getting Started

### Installing

pybadges can be installed using [pip][pip]:

```sh
pip install pybadges
```

To test that installation was successful, try:

```sh
python -m pybadges --left-text=build --right-text=failure --right-color='#c00' --browser
```

You will see a badge like this in your browser:

<p align="center">
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/build-failure.svg" />
</p>

## Usage

pybadges2 can be used both from the command line and as a Python library.

The command line interface is a great way to experiment with the API before
writing Python code.

You could also look at the [example server][example-server].

### Command line usage

Complete documentation of pybadges2 command arguments can be found using
the `--help` flag:

```sh
pybadges2 --help
 (or)
python -m pybadges2 --help
```

But the following usage demonstrates every interesting option:

```sh
pybadges2 \
    --left-text=complete \
    --right-text=example \
    --left-color=green \
    --right-color='#fb3' \
    --left-link=http://www.complete.com/ \
    --right-link=http://www.example.com \
    --logo='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAD0lEQVQI12P4zwAD/xkYAA/+Af8iHnLUAAAAAElFTkSuQmCC' \
    --embed-logo \
    --whole-title="Badge Title" \
    --left-title="Left Title" \
    --right-title="Right Title" \
    --browser
```

<p align="center">
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/complete.svg" />
</p>

#### A note about `--logo` and `--embed-logo`

> [!NOTE]
> Logos that are not embedded may experience issues on sites where the
> Content Security Policy (CSP) blocks the logo requests.

Note that the `--logo` option can attempt include a regular URL:

```sh
pybadges2 \
    --left-text="python" \
    --right-text="3.2, 3.3, 3.4, 3.5, 3.6" \
    --whole-link="https://www.python.org/" \
    --browser \
    --logo='https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg'
```

<p align="center">
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/python.svg" />
</p>

If the `--logo` option is set, the `--embed-logo` option can also be set.
The `--embed-logo` option causes the content of the URL provided in `--logo`
to be embedded in the badge rather than be referenced through a link.

The advantage of using this option is an extra HTTP request will not be
required to render the badge and that some browsers will not load image
references at all.

You may see the difference in your browser:

<p align="center">
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/embedded-logo.svg" />
    <img src="https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/no-embedded-logo.svg" />
</p>

#### A note about `--(whole|left|right)-title`

The `title` element is usually displayed as a [pop-up by browsers][svg-title]
but is currently [filtered by Github][github-markup-issue-1267].

### Library usage

pybadges is primarily meant to be used as a Python library.

```python
from pybadges2 import badge

s = badge(left_text='coverage', right_text='23%', right_color='red')
# s is a string that contains the badge data as an svg image.
print(s[:40]) # => <svg height="20" width="191.0" xmlns="ht
```

The keyword arguments to `badge()` are identical to the command flags names
described above except with keyword arguments using underscore instead of
hyphen/minus (e.g. `--left-text` => `left_text=`)

#### Server usage

pybadges2 can be used to serve badge images on the web.

[server-example][example-server] contains an example of serving badge
images from a [Flask server][flask].

### Caveats

- pybadges2 uses a pre-calculated table of text widths and [kerning][kerning]
  distances (for Western glyphs) to determine the size of the badge. Eastern
  European languages may be rendered less well than Western European ones:

  ![](https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/saying-russian.svg)

  And glyphs not present in Deja Vu Sans (the default font) may be rendered
  very poorly:

  ![](https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/saying-chinese.svg)

- pybadges2 does not have any explicit support for languages that are
  written right-to-left (e.g. Arabic, Hebrew) and the displayed text
  direction may be incorrect:

  ![](https://raw.githubusercontent.com/jdknight/pybadges2/refs/heads/main/tests/assets/golden-images/saying-arabic.svg)

## Development

Testing can be performed using [tox][tox]:

```sh
git clone https://github.com/jdknight/pybadges2.git
cd pybadges2
tox
```

Users wishing to contribute, please read the [contributor guide][contributing].


[badge-maker]: https://github.com/badges/shields/tree/master/badge-maker#badge-maker
[badges-shields-spec]: https://github.com/badges/shields/blob/master/spec/SPECIFICATION.md
[contributing]: https://github.com/jdknight/pybadges2/blob/main/CONTRIBUTING.md
[example-server]: https://github.com/jdknight/pybadges2/tree/main/server-example
[flask]: https://flask.palletsprojects.com/
[github-markup-issue-1267]: https://github.com/github/markup/issues/1267
[kerning]: https://wikipedia.org/wiki/Kerning
[pip]: https://pypi.org/project/pip/
[pybadges]: https://github.com/google/pybadges
[shields-io]: https://github.com/badges/shields
[svg-title]: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/title
[tox]: https://tox.wiki/
