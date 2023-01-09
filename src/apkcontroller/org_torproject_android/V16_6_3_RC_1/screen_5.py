"""Can be first screen after "Connection request" has been satisfied. The tor-
bridge is not yet started.

Presents a: "Connection request".
"""
# pylint: disable=R0801
import copy
from typing import Callable, Dict, List, Union

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.Screen import Screen


@typechecked
def screen_5(script_description: Dict[str, Union[bool, int, str]]) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 1
    description["screen_nr"] = 5
    description["wait_time_sec"] = 2
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
        {
            "@resource-id": "org.torproject.android:id/btnStart",
        },
        # Specific to this page.
        {
            "@text": "START",
        },
        {
            "@text": "Tor v0.4.7.11",
        },
    ]
    optional_objects: List[Dict[str, str]] = []

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
        return [actions_0, actions_1]

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=description,
        optional_objects=optional_objects,
    )


@typechecked
def actions_0(device: AutomatorDevice) -> None:
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
def actions_1(device: AutomatorDevice) -> None:
    """Performs the actions in option 2 in this screen."""
    # Press the START button in the Orbot app to create a tor connection.
    device(resourceId="org.torproject.android:id/btnStart").click()
