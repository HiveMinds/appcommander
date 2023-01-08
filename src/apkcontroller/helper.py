"""Contains helper functions that are used throughout this repository."""
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Union

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


def element_in_ui(
    wanted: Dict[str, Union[List, Dict]],
    screen: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all the keys and values in a dict are found within the
    same key or list of the xml of the ui."""
    if dict_contains_other_dict(wanted, screen):
        return True
    if "node" in screen.keys():
        if isinstance(screen["node"], Dict):
            if element_in_ui(wanted, screen["node"]):
                return True
        if isinstance(screen["node"], List):
            for node_elem in screen["node"]:
                if element_in_ui(wanted, node_elem):
                    return True
    return False


def dict_contains_other_dict(sub: Dict, main: Dict) -> bool:
    """Returns true if the sub dict is a subset of the main dict."""
    for sub_key, sub_val in sub.items():
        if sub_key not in main.keys():
            return False
        if sub_val != main[sub_key]:
            return False
    return True
