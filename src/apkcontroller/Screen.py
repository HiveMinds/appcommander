"""Starts a script to control an app."""

import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import (
    get_screen_as_dict,
    output_json,
    required_objects_in_screen,
)


# pylint: disable=R0902
class Screen:
    """Represents an Android app screen."""

    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        get_next_actions: Callable[
            [Dict[str, str], Dict[str, str]],
            List[Callable[[AutomatorDevice], None]],
        ],
        required_objects: List[Dict[str, str]],
        script_description: Dict[str, Union[bool, int, str]],
        optional_objects: Optional[List[Dict[str, str]]] = None,
        device: Optional[AutomatorDevice] = None,
    ) -> None:

        self.device: AutomatorDevice = device
        self.get_next_actions: Callable[
            [Dict[str, str], Dict[str, str]],
            List[Callable[[AutomatorDevice], None]],
        ] = get_next_actions

        self.max_retries: int = int(script_description["max_retries"])

        """Sets the required objects for this screen.

        (If these objects are not found within the screen information
        returned by the device, the screen will not be recogniszed. If
        it is, the screen is recognised by the: is_expected_screen function.
        """
        self.required_objects: List[Dict[str, str]] = required_objects

        self.screen_dict: Union[None, Dict] = None
        if self.device is not None:
            self.screen_dict = get_screen_as_dict(self.device)

        self.script_description: Dict[
            str, Union[bool, int, str]
        ] = script_description
        """Some buttons/obtjects in the screen may appear depending on
        parameters that are not predictable in advance, e.g. whether some
        server responds or not.

        Yet some actions may depend on the presence and/or value of
        these objects. Hence they should be stored here.
        """
        self.optional_objects: Union[
            None, List[Dict[str, str]]
        ] = optional_objects

        self.wait_time_sec: int = int(script_description["max_retries"])

    @typechecked
    def is_expected_screen(
        self,
        device: AutomatorDevice,
    ) -> bool:
        """Custom verification per screen based on the optional and required
        objects in screen.

        Raise error if verification fails.
        """
        if self.screen_dict is None:
            self.screen_dict = get_screen_as_dict(device)
        if not required_objects_in_screen(
            self.required_objects, self.screen_dict
        ):
            for _ in range(0, self.max_retries):
                time.sleep(self.wait_time_sec)
                if required_objects_in_screen(
                    self.required_objects, self.screen_dict
                ):
                    return True
            return False
        return True

    @typechecked
    def export_screen_data(
        self,
        device: AutomatorDevice,
        overwrite: bool = False,
    ) -> None:
        """Writes a dict file to a .json file, and exports a screenshot."""
        output_dir = (
            (
                "src/apkcontroller/scripts/"
                + f'{self.script_description["app_name"]}'
                + f'/{self.script_description["version"]}/'
            )
            .replace(".", "_")
            .replace(" ", "_")
        )
        output_name = f'{self.script_description["screen_name"]}'

        for extension in [".json", ".png"]:
            output_path = f"{output_dir}{output_name}{extension}"
            if not Path(output_path).is_file() or overwrite:

                if extension == ".json":
                    if self.screen_dict is None:
                        self.screen_dict = get_screen_as_dict(device)
                    output_json(
                        output_dir, f"{output_name}.json", self.screen_dict
                    )
                if extension == ".png":
                    # device.takeScreenshot(output_path)
                    device.screenshot(output_path)

            # Verify the file exists.
            if not Path(output_path).is_file():
                raise Exception(
                    f"Error, filepath:{output_path} was not created."
                )

    def goto_next_screen(
        self, actions: List[str], next_screen_index: int
    ) -> int:
        """Performs the actions in the list and then goes to the next
        screen."""

        print(f"TODO: goto next screen.{actions}")
        return next_screen_index


@typechecked
def get_next_screen(
    current_screen_name: str,
    script_graph: nx.DiGraph,
    actions: List[Callable[[AutomatorDevice], None]],
) -> bool:
    """Gets the next expected screen."""

    neighbour_edges = []
    neighbour_names = []
    edge_actions = []

    for neighbour_name in nx.all_neighbors(script_graph, current_screen_name):
        # Get neighbours.
        neighbour_names.append(neighbour_name)

        # Get edges twoards neighbours. (Outgoing edges).
        neighbour_edges.append([current_screen_name, neighbour_name])

        # Get all action lists in all those outgoing edges.
        edge_actions.append(script_graph.edges[neighbour_edges[-1]].actions)

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
