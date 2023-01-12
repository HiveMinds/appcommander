"""The settings screen where apps are torified."""
# pylint: disable=R0801
import copy
from typing import Callable, Dict, List, Optional, Union

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.Screen import Screen
from src.apkcontroller.script_helper import (
    get_current_screen_unpacked,
    get_torified_item_index_dict,
    orbot_torifying_app_is_checked,
)


@typechecked
def screen_6(script_description: Dict) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 10
    description["screen_nr"] = 6
    description["wait_time_sec"] = 1
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
    # pylint: disable=W0613
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        history: Dict,  # pylint: disable=W0613
        script_description: Optional[Dict] = {},
    ) -> List[Callable[[AutomatorDevice, Dict[str, str]], Dict]]:
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
        optional_objects=optional_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(
    device: AutomatorDevice, additional_info: Dict[str, Union[str, bool]]
) -> Dict:
    """Performs the actions in option 2 in this screen."""

    # TODO: get button ids to click.
    for app_name, _ in additional_info.items():

        # Refresh the screen.
        device(descriptionMatches="Refresh Apps").click()

        # Reload the screen data.
        unpacked_screen_dict: Dict = get_current_screen_unpacked(device)

        if app_name == "DAVx5":
            searched_name = "DAVx⁵"
        # required_object:Dict[str,str] ={"@text": app_name}
        required_object: Dict[str, str] = {"@text": searched_name}
        item_dict = get_torified_item_index_dict(
            required_object, unpacked_screen_dict, {}
        )
        item_index = int(item_dict["@index"])
        # Click those buttons if they are not enabled..
        if not orbot_torifying_app_is_checked(item_dict):
            device(index=item_index).click()

    # Optional(Click refresh).
    # Refresh the screen.
    device(descriptionMatches="Refresh Apps").click()

    # Click back.
    device(descriptionContains="Navigate up").click()

    return {"torified": "True", "expected_screens": [5, 7]}
