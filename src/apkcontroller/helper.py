"""Contains helper functions that are used throughout this repository."""
from pathlib import Path
from pprint import pprint
from typing import Dict

import xmltodict
from typeguard import typechecked
from uiautomator import AutomatorDevice


@typechecked
def file_exists(filepath: str) -> bool:
    """Checks if file exists.

    :param string:
    """
    # TODO: Execute Path(string).is_file() directly instead of calling this
    # function.
    my_file = Path(filepath)
    return my_file.is_file()


@typechecked
def show_screen_as_dict(d: AutomatorDevice) -> Dict:
    """Loads the phone and shows the screen as a dict.

    from uiautomator import device as d
    """
    print("Show screen data as dict:")

    doc = xmltodict.parse(d.dump())
    pprint(doc)
    print("Done")
    return doc
