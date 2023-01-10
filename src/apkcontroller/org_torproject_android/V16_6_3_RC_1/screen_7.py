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
def screen_7(script_description: Dict) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 1
    description["screen_nr"] = 7
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
            "@text": "STOP",
        },
        {
            "@content-desc": (
                "Orbot notification: Connected to the Tor network"
            )
        },
    ]
    optional_objects: List[Dict[str, str]] = []

    # pylint: disable=W0613
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        history: Dict,  # pylint: disable=W0613
    ) -> List[Callable[[AutomatorDevice, Dict[str, str]], None]]:
        """Looks at the required objects and optional objects and determines
        which actions to take next.
        An example of the next actions could be the following List:
        0. Select a textbox.
        1. Send some data to a textbox.
        2. Click on the/a "Next" button.

        Then the app goes to the next screen and waits a pre-determined
        amount, and optionally retries a pre-determined amount of attempts.
        """

        if (
            "desired_apps_are_torified" in history.keys()
            and history["desired_apps_are_torified"]
        ):
            # TODO: Set this screen as end screen, code is done.
            return []
        # Else:
        # Go to settings, and enable the required apps.
        return [actions_0]

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=description,
        optional_objects=optional_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(
    device: AutomatorDevice, additional_info: Dict[str, Union[str, bool]]
) -> None:
    """Go to settings inside Orbot to select which apps are torified."""
    device(resourceId="org.torproject.android:id/ivAppVpnSettings").click()
