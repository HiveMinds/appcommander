"""Starts a script to control an app."""

from typing import Callable, Dict, List, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice


# pylint: disable=R0902
# pylint: disable=R0903
class Screen:
    """Represents an Android app screen."""

    # pylint: disable=R0913
    # pylint: disable=W0102
    @typechecked
    def __init__(
        self,
        get_next_actions: Callable[
            [Dict[str, str], Dict[str, str], Dict[str, str]],
            Union[Callable[[AutomatorDevice, Dict[str, str]], Dict], None],
        ],
        required_objects: List[Dict[str, str]],
        script_description: Dict,
        optional_objects: List[Dict[str, str]] = [],
    ) -> None:
        self.get_next_actions: Callable[
            [Dict[str, str], Dict[str, str], Dict[str, str]],
            Union[Callable[[AutomatorDevice, Dict[str, str]], Dict], None],
        ] = get_next_actions

        # eloping typed dict.
        self.max_retries: int = int(str(script_description["max_retries"]))

        """Sets the required objects for this screen.

        (If these objects are not found within the screen information
        returned by the device, the screen will not be recogniszed. If
        it is, the screen is recognised by the: is_expected_screen function.
        """
        self.required_objects: List[Dict[str, str]] = required_objects

        self.script_description: Dict = script_description
        """Some buttons/obtjects in the screen may appear depending on
        parameters that are not predictable in advance, e.g. whether some
        server responds or not.

        Yet some actions may depend on the presence and/or value of
        these objects. Hence they should be stored here.
        """
        self.optional_objects: Union[
            None, List[Dict[str, str]]
        ] = optional_objects

        # eloping typed dict.
        self.wait_time_sec: float = float(
            str(script_description["wait_time_sec"])
        )
        self.screen_dict: Dict = {}


@typechecked
def get_next_screen(
    current_screen_nr: str,
    script_graph: nx.DiGraph,
    actions: Union[Callable[[AutomatorDevice, Dict[str, str]], Dict], None],
) -> bool:
    """Gets the next expected screen."""

    neighbour_edges = []
    neighbour_names = []
    edge_actions = []

    for neighbour_name in nx.all_neighbors(script_graph, current_screen_nr):
        # Get neighbours.
        neighbour_names.append(neighbour_name)

        # Get edges twoards neighbours. (Outgoing edges).
        neighbour_edges.append([current_screen_nr, neighbour_name])

        # Get all action lists in all those outgoing edges.
        edge_actions.append(script_graph.edges[neighbour_edges[-1]].actions)

    # Verify the sought action list is in that list of lists, only once,
    # otherwise raise error.
    if actions not in edge_actions:
        raise LookupError(
            f"Error, the expected action list:{actions} was not in the "
            + f"available actions:{edge_actions}"
        )

    for edge in edge_actions:
        if edge.actions == actions:
            # Return the node of the next screen of the edge that contains the
            # sought action list.
            return edge[1]
    raise NotImplementedError(
        "This error should never be reached, look at code."
    )
