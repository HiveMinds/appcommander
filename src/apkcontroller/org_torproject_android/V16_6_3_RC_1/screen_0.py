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
def screen_0(script_description: Dict[str, Union[bool, int, str]]) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 1
    description["screen_nr"] = 0
    description["wait_time_sec"] = 2
    required_objects: List[Dict[str, str]] = [
        {
            "@text": "Connection request",
        },
    ]

    # pylint: disable=W0613
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        history: Dict,
    ) -> List[Callable[[AutomatorDevice], None]]:
        """Looks at the required objects and optional objects and determines
        which actions to take next.
        An example of the next actions could be the following List:
        0. Select a textbox.
        1. Send some data to a textbox.
        2. Click on the/a "Next" button.

        Then the app goes to the next screen and waits a pre-determined
        amount, and optionally retries a pre-determined amount of attempts.
        TODO: Don't return a list of functions, just return one function,
        because this method should decide which action is to be performed based
        on the required and optional objects, and on nothing else.
        TODO: Determine how to deal with server responses/unpredictable input.
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
    """Performs the actions in option 1 in this screen. For this screen, it
    clicks the "OK" button in the "Connection request".

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
    device(resourceId="android:id/button1").click()
