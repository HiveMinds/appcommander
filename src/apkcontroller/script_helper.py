"""Functions to assist a script file for an arbitrary app."""
from typing import TYPE_CHECKING, Dict, List, Tuple, Union, cast

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import (
    dict_contains_other_dict,
    export_screen_data,
    get_screen_as_dict,
    is_expected_screen,
)

# pylint: disable=R0801
if TYPE_CHECKING:
    from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.Apk_script import (
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
    dev: AutomatorDevice,
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
            dev=dev,
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
def can_proceed(
    dev: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script: Apk_script,
) -> Tuple[bool, int]:
    """Checks whether the screen is expected, raises an error if not.

    And it returns the current screen number.
    """
    # get current screen dict.
    unpacked_screen_dict: Dict = get_screen_as_dict(
        dev=dev,
        unpack=True,
        screen_dict={},
        reload=False,
    )

    # verify current_screen in next_screens.
    is_expected, screen_nr = current_screen_is_expected(
        dev=dev,
        expected_screennames=expected_screennames,
        retry=retry,
        script_graph=script.script_graph,
        unpacked_screen_dict=unpacked_screen_dict,
    )

    # end_screens = get end_screens()
    if not is_expected:
        # Export the actual screen, screen data and expected screens in
        # specific error log folder.
        export_screen_data(
            dev=dev,
            screen_dict=unpacked_screen_dict,
            script_description=script.script_description,
            overwrite=True,
            subdir="error",
        )
        raise ReferenceError(
            f"Error, the expected screen was not found in:{screen_nr}. "
            + f"Searched for:{expected_screennames}. The accompanying screen "
            + "and xml can be found in:src/apkcontroller/<package_name>/<app_"
            + f'version>/error/{script.script_description["screen_nr"]}.json'
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

def get_expected_screen_nrs(
    G: nx.DiGraph, screen_nr: int, action_nr: int
) -> List[int]:
    """Returns the expected screens per screen per action."""
    expected_screens: List[int] = []
    for edge in G.edges:
        if edge[0] == screen_nr:
            if action_nr in G[edge[0]][edge[1]]["actions"]:
                expected_screens.append(edge[1])
    return expected_screens