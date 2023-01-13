"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""

from typing import TYPE_CHECKING, Dict, List

import networkx as nx
from typeguard import typechecked

from src.appcommander.create_screens import create_screens
from src.appcommander.org_torproject_android.V16_6_3_RC_1.screen_flow import (
    Script_flow,
)

if TYPE_CHECKING:
    from src.appcommander.Screen import Screen
else:
    Screen = object


# pylint: disable=R0902
class Script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903
    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        app_name: str,
        overwrite: bool,
        package_name: str,
        torifying_apps: Dict[str, str],
        version: str,
    ) -> None:
        self.app_name: str = app_name
        self.overwrite: bool = overwrite
        self.package_name: str = package_name
        self.torifying_apps: Dict[str, str] = torifying_apps
        self.version: str = version

        # Create placeholder for past screens.
        self.past_screens: List[int] = []

        # Generate the script screen flow as a graph and generate the screens.
        self.script_graph = Script_flow().G
        self.screens: List[Screen] = create_screens(self.script_graph)

        # Specify the start and end nodes in the graph.
        self.set_start_nodes(self.script_graph)

    @typechecked
    def set_start_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the is_start attributes to True in the nodes that are start
        screens."""

        for nodename in script_graph.nodes:
            screen: Screen = script_graph.nodes[nodename]["Screen"]
            if screen.screen_nr in list(range(0, 8)):
                script_graph.nodes[nodename]["is_start"] = True
            else:
                script_graph.nodes[nodename]["is_start"] = False
