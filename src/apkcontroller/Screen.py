"""Starts a script to control an app."""

from typing import Dict, List

import networkx as nx
from typeguard import typechecked


class Screen:
    """Represents an Android app screen."""

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
        wait_time_sec: int,
        max_retries: int,
    ) -> None:

        self.required_objects: Dict[str, str]
        self.optional_objects: Dict[str, str]
        self.wait_time_sec: int = wait_time_sec
        self.max_retries: int = max_retries

    @typechecked
    def verify_screen(self) -> None:
        """Custom verification per screen based on the optional and required
        objects in screen. Raise error if verification fails.

        TODO: include wait_time_sec and max_retries in verification.
        """
        print("TODO: implement verification.")

    @typechecked
    def export_screen_data(self) -> None:
        """Optional: export data from screen if relevant.

        TODO: include wait_time_sec and max_retries in export."""
        print("TODO: implement export option to log file.")

    @typechecked
    def get_next_actions(self) -> List[Action]:
        """Looks at the required objects and optinoal objects and determines
        which actions to take next.

        An example of the next actions could be the following List:
        0. Select a textbox.
        1. Send some data to a textbox.
        2. Click on the/a "Next" button.

        Then the app goes to the next screen and waits a pre-determined
        amount, and optionally retries a pre-determined amount of attempts.

        TODO: determine how to put this unique function on the right node.
        """
        print(
            "TODO: determine how to specify how to compute the next action"
            + " per screen."
        )

    @typechecked
    def get_next_screen(self, actions: List[Action]) -> nx.node:
        """Gets the next expected screen."""

        print("TODO: get next screen.")
        # Get neighbours.

        # Get edges twoards neighbours. (Outgoing edges).

        # Get all action lists in all those outgoing edges.

        # Verify the sought action list is in that list of lists, otherwise
        # raise error.

        # Return the edge(screen) of contains the sought action list.

    def goto_next_screen(
        self, actions: List[Action], next_screen: nx.node
    ) -> nx.node:
        """Performs the actions in the list and then goes to the next
        screen."""

        print("TODO: goto next screen.")
