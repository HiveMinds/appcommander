"""The settings screen where apps are torified."""
# pylint: disable=R0801
import copy
import inspect
from typing import Callable, Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_flow import (
    get_expected_screen_nrs,
)
from src.apkcontroller.Screen import Screen
from src.apkcontroller.script_helper import (
    get_screen_as_dict,
    get_torified_item_index_dict,
    orbot_torifying_app_is_checked,
)


@typechecked
def screen_6(script_description: Dict) -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    description = copy.deepcopy(script_description)
    description["max_retries"] = 5
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
    # pylint: disable=W0613
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        history: Dict,  # pylint: disable=W0613
        script_description: Optional[Dict] = {},
    ) -> Union[Callable[[AutomatorDevice, Dict[str, str]], Dict]]:
        """Looks at the required objects and optional objects and determines
        which actions to take next.
        An example of the next actions could be the following List:
        0. Select a textbox.
        1. Send some data to a textbox.
        2. Click on the/a "Next" button.

        Then the app goes to the next screen and waits a pre-determined
        amount, and optionally retries a pre-determined amount of attempts.
        """

        return actions_0

    return Screen(
        get_next_actions=get_next_actions,
        required_objects=required_objects,
        script_description=description,
        optional_objects=optional_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(device: AutomatorDevice, additional_info: Dict) -> Dict:
    """Performs the actions in option 2 in this screen."""

    torifying_apps = additional_info["torifying_apps"]

    # TODO: get button ids to click.
    for app_name, _ in torifying_apps.items():

        # Refresh the screen.
        device(descriptionMatches="Refresh Apps").click()

        # Reload the screen data.
        unpacked_screen_dict: Dict = get_screen_as_dict(
            device=device,
            unpack=True,
            screen_dict={},
            reload=True,
        )

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

    action_nr: int = int(inspect.stack()[0][3][8:])
    print(f"action_nr={action_nr}")
    screen_nr: int = additional_info["screen_nr"]
    script_flow: nx.DiGraph = additional_info["script_graph"]
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
