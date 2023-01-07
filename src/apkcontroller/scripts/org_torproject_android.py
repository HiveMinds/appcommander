"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""


import networkx as nx
from typeguard import typechecked

from src.apkcontroller.Screen import Screen


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
    ) -> None:

        self.name = "org.torproject.android"
        self.display_name = "Orbot"
        self.version = "16.6.3 RC 1"

        self.screens = nx.DiGraph()
        self.create_screens(self.screens)

    @typechecked
    def create_screens(self, screens: nx.DiGraph) -> None:
        """Creates the screens as networkx nodes."""

        screen = Screen(wait_time_sec=2, max_retries=3)
        screen.get_next_actions(
            screen.required_objects, screen.optional_objects
        )
        print(f"TODO: create screens{screens}")

    def specify_start_nodes(self, screens: nx.DiGraph) -> None:
        """Sets the start_nodes attributes to True in the nodes that are start
        screens."""
        print(f"TODO: set start node properties.{screens}")

    def specify_end_nodes(self, screens: nx.DiGraph) -> None:
        """Sets the end_nodes attributes to True in the nodes that are end
        screens."""
        print(f"TODO: set end node properties.{screens}")

    def create_screen_transitions(self, screens: nx.DiGraph) -> None:
        """Adds the edges between the nodes(screens), representing possible
        transitions between the screens. The edges contain a list containing
        lists of actions.

        For example, it may be that actions: [click: checkmark I, click:
        Next], lead to screen 3, as well as actions: [click: Next] lead
        to screen 3. Hence, 1 edge multiple action lists (in/as a list).
        """
        print(f"TODO: set edges properties.{screens}")
