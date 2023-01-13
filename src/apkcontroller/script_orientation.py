"""Functions to enable the app to know what the status of the phone is by
parsing screen data."""
from typing import TYPE_CHECKING, List

import networkx as nx
from typeguard import typechecked

# pylint: disable=R0801
if TYPE_CHECKING:
    from src.appcommander.org_torproject_android.V16_6_3_RC_1.Script import (
        Script,
    )
    from src.appcommander.Screen import Screen
else:
    Screen = object
    Script = object


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
def get_start_nodes(script_graph: nx.DiGraph) -> List[int]:
    """Sets the start_nodes attributes to True in the nodes that are start
    screens."""
    start_nodenames: List[int] = []
    for nodename in script_graph.nodes:
        if script_graph.nodes[nodename]["is_start"]:
            start_nodenames.append(nodename)
    return start_nodenames
