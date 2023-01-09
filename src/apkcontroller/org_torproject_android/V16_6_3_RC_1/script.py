"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""

from typing import Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import export_screen_data_if_valid
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_0 import (
    screen_0,
)
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_1 import (
    screen_1,
)
from src.apkcontroller.Screen import Screen


class Apk_script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903

    @typechecked
    def __init__(self, device: Optional[AutomatorDevice] = None) -> None:

        # Store data used to generate output and find Screen object files.
        self.script_description: Dict[str, Union[bool, int, str]] = {
            "title": "conf_orbot",
            "app_name": "org.torproject.android",
            "app_display_name": "Orbot",
            "version": "16.6.3 RC 1",
            "overwrite": True,
        }

        # Generate the script screen flow as a graph and generate the screens.
        self.script_graph = nx.DiGraph()
        self.screen_objects: List[Screen] = self.create_screen_objects(
            self.script_graph
        )

        # Export the data of the screens if they happen to be found in the
        # device already.
        if device is not None:
            export_screen_data_if_valid(
                device=device,
                overwrite=self.script_description["overwrite"],
                screen_objects=self.screen_objects,
            )

        # Specify the start and end nodes in the graph.
        self.specify_start_nodes(self.script_graph)

        # Specify the end and end nodes in the graph.
        self.specify_end_nodes(self.script_graph)

    @typechecked
    def create_screen_objects(self, script_graph: nx.DiGraph) -> List[Screen]:
        """Creates the screens as networkx nodes."""
        screen_objects: List[Screen] = []

        # Create screens.
        screen_objects.append(screen_0(self.script_description))
        screen_objects.append(screen_1(self.script_description))
        print(f"TODO: create all screens{script_graph}")
        return screen_objects

    @typechecked
    def specify_start_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the start_nodes attributes to True in the nodes that are start
        screens."""
        print(f"TODO: set start node properties.{script_graph}")
        for nodename in script_graph.nodes:
            screen: Screen = script_graph.nodes[nodename].graph["Screen"]
            if screen.script_description["screen_nr"] in [0, 1, 2, 3]:
                script_graph.nodes[nodename].graph["is_start"] = True

    @typechecked
    def specify_end_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the end_nodes attributes to True in the nodes that are end
        screens."""
        print(f"TODO: set end node properties.{script_graph}")

    @typechecked
    def create_screen_transitions(self, script_graph: nx.DiGraph) -> None:
        """Adds the edges between the nodes(screens), representing possible
        transitions between the screens. The edges contain a list containing
        lists of actions.

        For example, it may be that actions: [click: checkmark I, click:
        Next], lead to screen 3, as well as actions: [click: Next] lead
        to screen 3. Hence, 1 edge multiple action lists (in/as a list).
        """
        print(f"TODO: set edges properties.{script_graph}")
