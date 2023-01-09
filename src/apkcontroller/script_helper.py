"""Functions to assist a script file for an arbitrary app."""
from typing import Dict, List

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import get_screen_as_dict


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
def get_current_screen(device: AutomatorDevice) -> Dict:
    """Returns the meaningful dict from the phone UI."""
    # Load and unpack the screen dict to get meaningful ui info.
    screen_dict: Dict = get_screen_as_dict(device)
    unpacked_screen_dict: Dict = screen_dict["hierarchy"]
    return unpacked_screen_dict


@typechecked
def current_screen_is_expected(
    screen_dict: Dict, script_graph: nx.DiGraph
) -> Dict:
    """Determines whether the current screen is one of the expected screens."""
    print(script_graph)
    return screen_dict
