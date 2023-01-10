"""The settings screen where apps are torified."""
# pylint: disable=R0801
import copy
from pprint import pprint
from typing import Callable, Dict, List, Optional, Union

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.Screen import Screen
from src.apkcontroller.script_helper import (
    get_current_screen_unpacked,
    get_torified_item_buttons,
)


@typechecked
def screen_6(
    script_description: Dict[str, Union[bool, int, str, Dict[str, str]]]
) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 1
    description["screen_nr"] = 6
    description["wait_time_sec"] = 2
    required_objects: List[Dict[str, str]] = [
        # {
        # "@text": "Global " "(Auto)",
        # },
        {
            "@resource-id": "org.torproject.android:id/itemicon",
        },
        {
            "@resource-id": "org.torproject.android:id/itemtext",
        },
        {
            "@resource-id": "org.torproject.android:id/itemcheck",
        },
    ]
    optional_objects: List[Dict[str, str]] = []

    # pylint: disable=W0102
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        history: Dict,  # pylint: disable=W0613
        script_description: Optional[Dict] = {},
    ) -> List[Callable]:
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
        print(f"history={history}")
        print(f"script_description={script_description}")
        return [actions_1]

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=description,
        optional_objects=optional_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(
    device: AutomatorDevice, additional_info: Dict[str, str]
) -> None:
    """TODO."""
    # Go to settings to select which apps are torified.
    device(resourceId="org.torproject.android:id/ivAppVpnSettings").click()


# pylint: disable=W0613
@typechecked
def actions_1(
    device: AutomatorDevice, additional_info: Dict[str, str]
) -> None:
    """Performs the actions in option 2 in this screen."""
    unpacked_screen_dict: Dict = get_current_screen_unpacked(device)

    # TODO: get button ids to click.
    for app_name, package_name in additional_info.items():
        print(f"torifying app_name={app_name}")
        print(f"torifying package_name={package_name}")
        print(f"device={device}")
        if app_name == "DAVx5":
            searched_name = "DAVx⁵"
        # required_object:Dict[str,str] ={"@text": app_name}
        required_object: Dict[str, str] = {"@text": searched_name}
        returned_value = get_torified_item_buttons(
            required_object, unpacked_screen_dict
        )
        print("returned_value=")
        pprint(returned_value)
    # Click those buttons.

    # Optional(Click refresh).

    # Click back.

    raise Exception("Not built yet.")
