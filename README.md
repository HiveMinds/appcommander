# Control Android Apps from Python

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3106/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code Coverage](https://codecov.io/gh/a-t-0/snn/branch/main/graph/badge.svg)](https://codecov.io/gh/a-t-0/snnalgorithms)

Uses `uiautomator` to automatically and safely control and navigate Android
apps.
The user can specify some app logic (series of screens and button clicks) that
is executed on your Android phone through ADB.

## Example

TODO

## Usage

First satisfy the prerequisites:

```bash
pip install apkcontroller
```

Connect your phone, and tell this code which app you want to automate, and how:

```bash
python -m src.apkcontroller -a org.torproject.android -v 0.4.7.11 -s initiate.py
```

which is the same as:

```bash
python -m src.apkcontroller --app-name \
org.torproject.android --version 0.4.7.11 --script initiate.py
```

For more info, run:

```bash
python -m src.apkcontroller --help
```

And run tests with:

```bash
python -m pytest
```

or to see live output, on any tests filenames containing substring: `results`:

```bash
python -m pytest --capture=tee-sys

```

## Test Coverage

Developers can use:

```bash
conda env create --file environment.yml
conda activate apkcontroller
python -m pytest
```

Currently the test coverage is `65%`. For type checking:

```bash
mypy --disallow-untyped-calls --disallow-untyped-defs tests/some_test.py
```

### Releasing pip package update

To udate the Python pip package, one can first satisfy the following requirements:

```bash
pip install --upgrade pip setuptools wheel
pip install twine
```

Followed by updating the package with:

```bash
python3 setup.py sdist bdist_wheel
python -m twine upload dist/\*
```

### Developer pip install

```bash
mkdir -p ~/bin
cp apk-ct.sh ~/bin/apk-ct
chmod +x ~/bin/apk-ct
```

Then you can rebuild and locally re-install the `apkcontroller` pip package the command:

```bash
apk-ct
```

If you want to quickly test if your changes work, you can go into the root dir
of this project and run:

```bash
pip install -e .
```

that installs the latest changes into the pip package locally (into your conda
environment).

<!-- Un-wrapped URL's (Badges and Hyperlinks) -->
