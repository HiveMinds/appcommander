"""First entry point on app if it is freshly installed.

Presents a: "Connection Request".
"""
# pylint: disable=R0801
import copy
from typing import Callable, Dict, List, Union

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.Screen import Screen


@typechecked
def screen_2(script_description: Dict[str, Union[bool, int, str]]) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 1
    description["screen_nr"] = 2
    description["wait_time_sec"] = 2
    required_objects: List[Dict[str, str]] = [
        {
            "@text": "Browse the internet how you expect you should.",
        },
        {
            "@text": "No tracking. No censorship.",
        },
    ]

    # pylint: disable=W0613
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

        return [actions_0]

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=description,
        optional_objects=[],
    )


@typechecked
def actions_0(device: AutomatorDevice) -> None:
    """Performs the actions in option 0 in this screen.

    For this screen, it clicks the "Next" button (icon=">") in the
    bottom right.
    """
    device(resourceId="org.torproject.android:id/next").click()
