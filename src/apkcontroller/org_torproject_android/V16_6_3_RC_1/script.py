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
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_2 import (
    screen_2,
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
        self.screens: List[Screen] = self.create_screens(self.script_graph)

        # Export the data of the screens if they happen to be found in the
        # device already.
        if device is not None:
            export_screen_data_if_valid(
                device=device,
                overwrite=self.script_description["overwrite"],
                screens=self.screens,
            )

        # Specify the start and end nodes in the graph.
        self.specify_start__and_end_nodes(self.script_graph)

    @typechecked
    def create_screens(self, script_graph: nx.DiGraph) -> List[Screen]:
        """Creates the screens as networkx nodes."""
        screens: List[Screen] = []

        # Create screens.
        screens.append(screen_0(self.script_description))
        screens.append(screen_1(self.script_description))
        screens.append(screen_2(self.script_description))

        for screen in screens:
            script_graph.add_node(screen.script_description["screen_nr"])
            script_graph.nodes[screen.script_description["screen_nr"]][
                "Screen"
            ] = screen
        return screens

    @typechecked
    def specify_start__and_end_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the is_start attributes to True in the nodes that are start
        screens.

        Sets the is_end attributes to True in the nodes that are end
        screens.
        """

        for nodename in script_graph.nodes:
            screen: Screen = script_graph.nodes[nodename]["Screen"]
            if screen.script_description["screen_nr"] in [0, 1, 2]:
                script_graph.nodes[nodename]["is_start"] = True
            if screen.script_description["screen_nr"] in [1, 2]:
                script_graph.nodes[nodename]["is_end"] = True

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
