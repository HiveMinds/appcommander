# Command Android Apps from Python

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3106/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code Coverage](https://codecov.io/gh/a-t-0/snn/branch/main/graph/badge.svg)](https://codecov.io/gh/a-t-0/snnalgorithms)

Uses `uiautomator` to automatically and safely control and navigate Android
apps.
The user can specify some app logic (series of screens and button clicks) that
is executed on your Android phone through ADB.

## Why
I wanted self-host my Nextcloud calendar with 1 command, from anywhere in the world, no port-forwarding, no DNS stuff, no domain-name, no registrar configruation no nothing. That includes complete Android phone configuration automation for me. Some apps did not have, and perhaps may not want, a configuration API. Configuring Android apps with automated key-presses is not safe because an unexpected event may come up, e.g. a prompt for a phone update, a call may come in etc.

So I wanted a safe- and controlled way to configure the app, using the UI. This repository verifies each step in an arbitrary script, verifies the button is the desired button etc. If unexpected changes are expected, the script aborts.

Also, each phone manufacturer has a different rooting process, this repo can become a library to safely- and automatically root all (rootable) Android phones automatically (except the user must enable `ADB` themselves).

## Example

![image](https://user-images.githubusercontent.com/34750068/212434675-65839344-0dbd-43c1-a7c2-3717cdd40d31.png)


## Usage

First satisfy the prerequisites:

```bash
pip install apkcontroller
```

Connect your phone, and tell this code which app you want to automate, and how:

```bash
python -m src.apkcontroller -a org.torproject.android -v "16.6.3 RC 1" -t "DAVx5"
```

which is the same as:

```bash
python -m src.apkcontroller --app-name org.torproject.android \
--version "16.6.3 RC 1" -torify "DAVx5"
```

For more info, run:

```bash
python -m src.apkcontroller --help
```

## Testing

One can simulate an android phone with:

```sh
chmod +x emulate_android.sh
./emulate_android.sh
```

And then launch the emulated android phone with:

```sh
. ~/.profile
cd ~/.android/avd/android-small.avd/
rm *.lock
emulator -avd android-small -netdelay none -netspeed full -skin 768x1280
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
