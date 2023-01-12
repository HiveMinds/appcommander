"""Functions to assist a script file for an arbitrary app."""
import time
from pprint import pprint
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union, cast

import networkx as nx
import xmltodict
from typeguard import typechecked
from uiautomator import AutomatorDevice

if TYPE_CHECKING:
    from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
        Apk_script,
    )
    from src.apkcontroller.Screen import Screen
else:
    Screen = object
    Apk_script = object


@typechecked
def get_start_nodes(script_graph: nx.DiGraph) -> List[int]:
    """Sets the start_nodes attributes to True in the nodes that are start
    screens."""
    start_nodenames: List[int] = []
    for nodename in script_graph.nodes:
        if script_graph.nodes[nodename]["is_start"]:
            start_nodenames.append(nodename)
    return start_nodenames


@typechecked
def get_expected_screens(
    expected_screennames: List[int], script_graph: nx.DiGraph
) -> List[Screen]:
    """Determines whether the current screen is one of the expected screens."""
    expected_screens: List[Screen] = []
    for nodename in script_graph.nodes:
        if nodename in expected_screennames:
            expected_screens.append(script_graph.nodes[nodename]["Screen"])

    return expected_screens


@typechecked
def current_screen_is_expected(
    device: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script_graph: nx.DiGraph,
    unpacked_screen_dict: Dict,
) -> Tuple[bool, int]:
    """Determines whether the current screen is one of the expected screens."""
    expected_screens: List[Screen] = get_expected_screens(
        expected_screennames, script_graph
    )
    for expected_screen in expected_screens:
        if is_expected_screen(
            device=device,
            expected_screen=expected_screen,
            retry=retry,
            unpacked_screen_dict=unpacked_screen_dict,
        ):

            return (
                True,
                int(str(expected_screen.script_description["screen_nr"])),
            )
    return (False, -1)


@typechecked
def is_expected_screen(
    device: AutomatorDevice,
    expected_screen: Screen,
    retry: bool,
    unpacked_screen_dict: Dict,
    verbose: Optional[bool] = False,
) -> bool:
    """Custom verification per screen based on the optional and required
    objects in screen.

    Raise error if verification fails.
    """
    # Preliminary check to see if the required objects are in.
    if not required_objects_in_screen(
        expected_screen.required_objects, unpacked_screen_dict
    ):
        if not retry:
            return False
        # Retry and return True if the required objects were found.
        for _ in range(0, expected_screen.max_retries):

            # Reload the screen data again.
            unpacked_screen_dict = get_screen_as_dict(
                device=device,
                unpack=True,
                screen_dict={},
                reload=True,
            )

            time.sleep(expected_screen.wait_time_sec)
            if required_objects_in_screen(
                required_objects=expected_screen.required_objects,
                unpacked_screen_dict=unpacked_screen_dict,
            ):
                return True
            if verbose:
                print(f"Not found:{expected_screen.required_objects}")
        if verbose:
            print(f"Not found:{expected_screen.required_objects}")
        return False
    # else:
    return True


@typechecked
def required_objects_in_screen(
    required_objects: List[Dict[str, Union[List, Dict, str]]],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all required objects are found in the UI/screen.

    False otherwise.
    """
    for required_object in required_objects:
        if not required_object_in_screen(
            required_object=required_object,
            unpacked_screen_dict=unpacked_screen_dict,
        ):
            return False
    return True


@typechecked
def get_screen_as_dict(
    device: AutomatorDevice,
    unpack: bool,
    screen_dict: Dict,
    reload: bool = False,
) -> Dict:
    """Loads the phone and shows the screen as a dict."""

    # Don't reload if the screen dict still exists, and no explicit
    # reload is asked.
    if screen_dict != {} and not reload:
        if unpack and "hierarchy" in screen_dict.keys():
            return screen_dict["hierarchy"]
        return screen_dict

    # Get the new screen data from the ui.
    if screen_dict == {} or reload:
        print("Loading screen data from phone for orientation.")
        ui_information: Dict = xmltodict.parse(device.dump())

        # Unpack the screen dict to get a recursive dictionary structure.
        if unpack:
            ui_information = ui_information["hierarchy"]
    return ui_information


@typechecked
def required_object_in_screen(
    required_object: Dict[str, Union[List, Dict, str]],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all the keys and values in a dict are found within the
    same key or list of the xml of the ui."""
    if dict_contains_other_dict(required_object, unpacked_screen_dict):
        return True
    if "node" in unpacked_screen_dict.keys():
        if isinstance(unpacked_screen_dict["node"], Dict):
            if required_object_in_screen(
                required_object=required_object,
                unpacked_screen_dict=unpacked_screen_dict["node"],
            ):
                return True
        if isinstance(unpacked_screen_dict["node"], List):
            for node_elem in unpacked_screen_dict["node"]:
                if required_object_in_screen(
                    required_object=required_object,
                    unpacked_screen_dict=node_elem,
                ):
                    return True
        if not isinstance(unpacked_screen_dict["node"], Dict | List):
            raise TypeError("Node value of unexpected type.")
    return False


@typechecked
def get_torified_item_index_dict(
    required_object: Dict[str, str],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
    parent_dict: Union[List, Dict[str, Union[List, Dict, str]]],
) -> Dict:  # -> Dict[str, str]:
    """Parses the screen dictionary and returns the index of the item of the
    app that you want to torify. The item is found by checking if it has a
    "node" key, which has a List of 3 elements as value (each in the form of a
    dict):
     - the app icon.
     - the app name
     - the checkbox to torify that app.
    The dict with the app name is used to identify the relevant item, then the
    dictionary of that item contains the @index value, which is the index of
    that app in the Orbot configuration/torify apps screen. This method returns
    the complete item dictionary including the 3 node children.

    It recursively looks through the screen dict until it has found the app."""

    if dict_contains_other_dict(required_object, unpacked_screen_dict):
        return cast(Dict, parent_dict)
    if "node" in unpacked_screen_dict.keys():
        if isinstance(unpacked_screen_dict["node"], Dict):
            if get_torified_item_index_dict(
                required_object=required_object,
                unpacked_screen_dict=unpacked_screen_dict["node"],
                parent_dict=unpacked_screen_dict,
            ):
                return get_torified_item_index_dict(
                    required_object=required_object,
                    unpacked_screen_dict=unpacked_screen_dict["node"],
                    parent_dict=unpacked_screen_dict,
                )
        if isinstance(unpacked_screen_dict["node"], List):

            # A item in the Orbot app consists of an icon, app_name and
            # checkbox. So if the length of this node List is three, and it
            # contains the app name in the dict of the first index of the list
            # elements, one wants the index of the actual dict that has this
            # node list, because that dict has the index of the item.
            if len(unpacked_screen_dict["node"]) == 3:
                if dict_contains_other_dict(
                    required_object, unpacked_screen_dict["node"][1]
                ):
                    return unpacked_screen_dict

            # Keep on searching deeper otherwise.
            for node_elem in unpacked_screen_dict["node"]:
                if get_torified_item_index_dict(
                    required_object=required_object,
                    unpacked_screen_dict=cast(Dict, node_elem),
                    parent_dict=unpacked_screen_dict["node"],
                ):
                    return get_torified_item_index_dict(
                        required_object=required_object,
                        unpacked_screen_dict=cast(Dict, node_elem),
                        parent_dict=unpacked_screen_dict["node"],
                    )
        if not isinstance(unpacked_screen_dict["node"], Dict | List):
            raise TypeError("Node value of unexpected type.")
    return {}


@typechecked
def dict_contains_other_dict(sub: Dict, main: Dict) -> bool:
    """Returns true if the sub dict is a subset of the main dict."""
    for sub_key, sub_val in sub.items():
        if sub_key not in main.keys():
            return False
        # An artifact like:
        # "@text": "VPN Mode \u200e\u200f\u200e\u200e\u200e\u200e\u200e\u200f
        # \u200e\u200f\u200f\u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\
        # u200e\u200e\u200f\u200e\u200e\u200e\u200e\u200f\u200f\u200f\u200f\
        # u200f\u200e\u200e\u200f\u200f\u200e\u200e\u200e\u200f\u200e\u200e\
        # u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200f\u200f\
        # u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200f\u200e\
        # u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200e\u200e\u200e\
        # u200f\u200e\u200e\u200e\u200f\u200f\u200f\u200f\u200f\u200e\u200e\
        # u200f\u200f\u200e\u200f\u200f\u200e\u200e\u200e\u200eON\u200e\u200f
        # \u200e\u200e\u200f\u200e",
        # may occur at random. Therefore, the "in" option is included.
        # TODO: determine why these artifacts may occur and/or remove them.
        if sub_val != main[sub_key] and sub_val not in main[sub_key]:
            return False
    return True


@typechecked
def can_proceed(
    device: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script: Apk_script,
) -> Tuple[bool, int]:
    """Checks whether the screen is expected, raises an error if not.

    And it returns the current screen number.
    """
    # get current screen dict.
    unpacked_screen_dict: Dict = get_screen_as_dict(
        device=device,
        unpack=True,
        screen_dict={},
        reload=False,
    )

    # verify current_screen in next_screens.
    is_expected, screen_nr = current_screen_is_expected(
        device=device,
        expected_screennames=expected_screennames,
        retry=retry,
        script_graph=script.script_graph,
        unpacked_screen_dict=unpacked_screen_dict,
    )

    # end_screens = get end_screens()
    if not is_expected:
        pprint(unpacked_screen_dict)
        # TODO: Export the actual screen, screen data and expected screens in
        # specific error log folder.
        raise ReferenceError(
            f"Error, the expected screen was not found in:{screen_nr}."
            f"Searched for:{expected_screennames}."
        )
    return is_expected, screen_nr


def orbot_torifying_app_is_checked(app_item: Dict) -> bool:
    """Returns True if the item is checked, False if it is unchecked."""
    if "@checkable" not in app_item["node"][2].keys():
        raise KeyError(
            "Error, the app checkbox should contain @checkable."
            + f"Though it did not:{app_item}"
        )
    if "@checkable" not in app_item["node"][2]["@checkable"] != "true":
        raise ValueError(
            "Error, the app checkbox should contain:"
            + f"@checkable: true Though it did not:{app_item}"
        )
    if app_item["node"][2]["@checked"] == "true":
        return True
    if app_item["node"][2]["@checked"] == "false":
        return False
    raise KeyError(
        "Error, valid @checked value was not found in app_item checkbox."
    )
