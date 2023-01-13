"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""

from typing import TYPE_CHECKING, Dict, List, Optional

import networkx as nx
from typeguard import typechecked

from src.apkcontroller.create_screens import create_screens
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_flow import (
    Script_flow,
)

if TYPE_CHECKING:
    from src.apkcontroller.Screen import Screen

else:
    Screen = object


class Apk_script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
        torifying_apps: Optional[Dict[str, str]] = None,
    ) -> None:

        # Store data used to generate output and find Screen object files.
        self.script_description: Dict = {
            "title": "conf_orbot",
            "app_name": "org.torproject.android",
            "app_display_name": "Orbot",
            "version": "16.6.3 RC 1",
            "overwrite": True,
        }
        if torifying_apps is not None:
            self.script_description["torifying_apps"] = torifying_apps

        # Generate the script screen flow as a graph and generate the screens.
        self.script_graph = Script_flow().G
        self.screens: List[Screen] = create_screens(self, self.script_graph)

        # Specify the start and end nodes in the graph.
        self.set_start_nodes(self.script_graph)

    @typechecked
    def set_start_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the is_start attributes to True in the nodes that are start
        screens."""

        for nodename in script_graph.nodes:
            screen: Screen = script_graph.nodes[nodename]["Screen"]
            if screen.script_description["screen_nr"] in list(range(0, 8)):
                script_graph.nodes[nodename]["is_start"] = True
            else:
                script_graph.nodes[nodename]["is_start"] = False
