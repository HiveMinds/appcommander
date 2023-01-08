"""Starts a script to control an app."""

from typing import Any, Callable, Dict, List, Optional

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import show_screen_as_dict


class Screen:
    """Represents an Android app screen."""

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
        get_next_actions: Callable[
            [Dict[str, Any], Dict[str, Any]],
            List[Callable[[AutomatorDevice], None]],
        ],
        max_retries: int,
        required_objects: List[Dict[str, Any]],
        wait_time_sec: int,
        optional_objects: Optional[List[Dict[str, Any]]] = None,
    ) -> None:

        self.get_next_actions: Callable[
            [Dict[str, Any], Dict[str, Any]],
            List[Callable[[AutomatorDevice], None]],
        ] = get_next_actions

        self.max_retries: int = max_retries

        """Sets the required objects for this screen.

        (If these objects are not found within the screen information
        returned by the device, the screen will not be recogniszed. If
        it is, the screen is recognised by the: is_screen function.
        """
        self.required_objects: List[Dict[str, Any]] = required_objects
        """Some buttons/obtjects in the screen may appear depending on
        parameters that are not predictable in advance, e.g. whether some
        server responds or not.

        Yet some actions may depend on the presence and/or value of
        these objects. Hence they should be stored here.
        """
        self.optional_objects: List[Dict[str, Any]] = optional_objects

        self.wait_time_sec: int = wait_time_sec

    @typechecked
    def is_screen(self, d: AutomatorDevice) -> bool:
        """Custom verification per screen based on the optional and required
        objects in screen. Raise error if verification fails.

        TODO: include wait_time_sec and max_retries in verification.
        """
        screen_dict = show_screen_as_dict(d)
        print(f"TODO: implement verification: {d}")

        for required_key, required_val in self.required_objects.items():
            if required_key not in screen_dict.keys():
                return False
            if required_val not in screen_dict.vals():
                return False
        return True

    @typechecked
    def export_screen_data(self, d: AutomatorDevice) -> Dict[str, Any]:
        """Optional: export data from screen if relevant.

        TODO: include wait_time_sec and max_retries in export."""
        print(f"TODO: implement export option to log file.{d}")
        return {"TODO": "TODO"}

    def goto_next_screen(
        self, actions: List[str], next_screen_index: int
    ) -> int:
        """Performs the actions in the list and then goes to the next
        screen."""

        print(f"TODO: goto next screen.{actions}")
        return next_screen_index


@typechecked
def get_next_screen(
    screen_name,
    screens: nx.DiGraph,
    actions: List[Callable[[AutomatorDevice], None]],
) -> bool:
    """Gets the next expected screen.

    TODO: add typing.
    """

    print("TODO: get next screen.")
    neighbour_edges = [], neighbour_names = [], edge_actions = []

    for neighbour_name in nx.all_neighbors(screens, screen_name):
        # Get neighbours.
        neighbour_names.append(neighbour_name)

        # Get edges twoards neighbours. (Outgoing edges).
        neighbour_edges.append([screen_name, neighbour_name])

        # Get all action lists in all those outgoing edges.
        edge_actions.append(screens.edges[neighbour_edges[-1]].actions)

    # Verify the sought action list is in that list of lists, only once,
    # otherwise raise error.
    if actions not in edge_actions:
        raise LookupError(
            f"Error, the expected action list:{actions} was not in the "
            + f"available actions:{edge_actions}"
        )

    # TODO: check if actions occurs more than once in edge_actions, if yes
    # raise exception.

    for edge in edge_actions:
        if edge.actions == actions:
            # Return the node of the next screen of the edge that contains the
            # sought action list.
            return edge[1]
    raise NotImplementedError(
        "This error should never be reached, look at code."
    )
