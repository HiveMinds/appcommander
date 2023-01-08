"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""

from typing import Callable, Dict, List, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice
from uiautomator import device as d

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

        self.script_description: Dict[str, Union[bool, int, str]] = {
            "title": "conf_orbot",
            "app_name": "org.torproject.android",
            "app_display_name": "Orbot",
            "version": "16.6.3 RC 1",
            "overwrite": True,
        }
        self.screens = nx.DiGraph()
        screens: List[Screen] = self.create_screens(self.screens)

        screens[0].export_screen_data(
            device=d, overwrite=self.script_description["overwrite"]
        )

    @typechecked
    def create_screens(self, screens: nx.DiGraph) -> List[Screen]:
        """Creates the screens as networkx nodes."""

        s0: Screen = org_torproject_android_s0(self.script_description)
        print(f"TODO: create all screens{screens}")
        return [s0]

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


def org_torproject_android_s0(
    script_description: Dict[str, Union[bool, int, str]]
) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""

    script_description["max_retries"] = 1
    script_description["screen_name"] = "s0"
    script_description["wait_time_sec"] = 2
    required_objects: List[Dict[str, str]] = [
        {
            "@text": "Global " "(Auto)",
        },
        {
            "@text": "Trouble " "connecting?",
        },
        {
            "@text": "Use Bridges ",
        },
        {
            "@text": "Orbot",
        },
    ]
    optional_objects: List[Dict[str, str]] = [
        # Append options that are visible when the screen is connected to tor.
        {
            "@content-desc": (
                "Orbot notification: Connected " + "to the Tor network"
            ),
            "@text": "STOP",
        }
    ]

    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
    ) -> List[Callable[[AutomatorDevice], None]]:
        """Looks at the required objects and optional objects and determines
        which actions to take next.
        An example of the next actions could be the following List:
        0. Select a textbox.
        1. Send some data to a textbox.
        2. Click on the/a "Next" button.

        Then the app goes to the next screen and waits a pre-determined
        amount, and optionally retries a pre-determined amount of attempts.
        """

        print(
            "TODO: determine how to specify how to compute the next action"
            + f" for this screen. {required_objects},{optional_objects}"
        )
        return [actions_1, actions_2]

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=script_description,
        optional_objects=optional_objects,
    )


@typechecked
def actions_1(device: AutomatorDevice) -> None:
    """Performs the actions in option 1 in this screen.

    Example:
    d(
        resourceId=resourceId,
        text=text,
        className=className,
        descriptionContains= descriptionContains,
        index=index,
        description=description
    ).click()
    """
    # Go to settings to select which apps are torified.
    device(resourceId="org.torproject.android:id/ivAppVpnSettings").click()


@typechecked
def actions_2(device: AutomatorDevice) -> None:
    """Performs the actions in option 2 in this screen."""
    # Press the START button in the Orbot app to create a tor connection.
    device(resourceId="org.torproject.android:id/btnStart").click()
