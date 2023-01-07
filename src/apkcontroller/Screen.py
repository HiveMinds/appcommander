"""Starts a script to control an app."""

from typing import Callable, Dict, List

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice


class Screen:
    """Represents an Android app screen."""

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
        wait_time_sec: int,
        max_retries: int,
    ) -> None:

        # Base properties
        self.wait_time_sec: int = wait_time_sec
        self.max_retries: int = max_retries

        # Custom.
        self.required_objects: Dict[str, str] = self.set_required_objects()
        self.optional_objects: Dict[str, str] = self.set_optional_objects()

    @typechecked
    def is_screen(self, d: AutomatorDevice) -> bool:
        """Custom verification per screen based on the optional and required
        objects in screen. Raise error if verification fails.

        TODO: include wait_time_sec and max_retries in verification.
        """
        print(f"TODO: implement verification: {d}")
        return True

    @typechecked
    def export_screen_data(self, d: AutomatorDevice) -> Dict[str, str]:
        """Optional: export data from screen if relevant.

        TODO: include wait_time_sec and max_retries in export."""
        print(f"TODO: implement export option to log file.{d}")
        return {"TODO": "TODO"}

    @typechecked
    def get_next_screen(self, screens: nx.DiGraph, actions: List[str]) -> bool:
        """Gets the next expected screen."""

        print("TODO: get next screen.")
        # Get neighbours.

        # Get edges twoards neighbours. (Outgoing edges).

        # Get all action lists in all those outgoing edges.

        # Verify the sought action list is in that list of lists, only once,
        # otherwise raise error.

        # Return the edge(screen) of contains the sought action list.
        print(f"TODO: {actions}")
        return screens.node[0]

    def goto_next_screen(
        self, actions: List[str], next_screen_index: int
    ) -> int:
        """Performs the actions in the list and then goes to the next
        screen."""

        print(f"TODO: goto next screen.{actions}")
        return next_screen_index

    @typechecked
    def set_required_objects(self) -> Dict[str, str]:
        """Sets the required objects for this screen.

        (If these objects are not found within the screen information
        returned by the device, the screen will not be recogniszed. If
        it is, the screen is recognised by the: is_screen function.
        """
        print("TODO: implement required objects.")
        return {"TODO": "TODO"}

    @typechecked
    def set_optional_objects(self) -> Dict[str, str]:
        """Some buttons/obtjects in the screen may appear depending on
        parameters that are not predictable in advance, e.g. whether some
        server responds or not.

        Yet some actions may depend on the presence and/or value of
        these objects. Hence they should be stored here.
        """
        print("TODO: implement optional objects.")
        return {"TODO": "TODO"}

    @typechecked
    def get_next_actions(
        self,
        required_objects: Dict[str, str],
        optional_objects: Dict[str, str],
    ) -> List[Callable[[AutomatorDevice], None]]:
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
            + f" for this screen. {required_objects},{optional_objects}"
        )
        return [actions_1, actions_2]


@typechecked
def actions_1(d: AutomatorDevice) -> None:
    """Performs the actions in option 1 in this screen."""
    print(f"TODO: perform actions 1.{d}")


@typechecked
def actions_2(d: AutomatorDevice) -> None:
    """Performs the actions in option 2 in this screen."""
    print(f"TODO: perform actions 2.{d}")
