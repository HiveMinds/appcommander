"""The settings screen where apps are torified."""
# pylint: disable=R0801
import inspect
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from appcommander.helper import get_screen_as_dict
from appcommander.org_torproject_android.V16_6_3_RC_1.helper import (
    get_torified_item_index_dict,
    orbot_torifying_app_is_checked,
)
from appcommander.Screen import Screen
from appcommander.script_orientation import get_expected_screen_nrs

if TYPE_CHECKING:
    from appcommander.Script import Script
else:
    Script = object


@typechecked
def screen_6() -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    max_retries = 5
    screen_nr = 6
    wait_time_sec = 2
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
        script: Script,  # pylint: disable=W0613
        script_description: Optional[Dict] = {},
    ) -> Union[Callable[[AutomatorDevice, Screen, Script], Dict], None]:
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
        is_start=True,
        get_next_actions=get_next_actions,
        max_retries=max_retries,
        screen_nr=screen_nr,
        wait_time_sec=wait_time_sec,
        required_objects=required_objects,
        optional_objects=optional_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(dev: AutomatorDevice, screen: Screen, script: Script) -> Dict:
    """Performs the actions in option 2 in this screen."""

    # Get the dictionary with apps that need to be torified.
    torifying_apps = script.input_data.torifying_apps

    if not isinstance(torifying_apps, Dict):
        raise TypeError(
            f"Error, torifying_apps not specified:{torifying_apps}"
        )
    for app_name, _ in torifying_apps.items():

        # Refresh the Orbot settings screen.
        dev(descriptionMatches="Refresh Apps").click()

        # Reload the screen data.
        unpacked_screen_dict: Dict = get_screen_as_dict(
            dev=dev,
            unpack=True,
            screen_dict={},
            reload=True,
        )

        # Map from normal function name, to name in UI xml for DAVx5 app.
        if app_name == "DAVx5":
            searched_name = "DAVx⁵"

        # Specify which dict element is required in the screen that contains
        # the app that needs to be torified.
        required_object: Dict[str, str] = {"@text": searched_name}

        # The dict that contains the app that needs to be torified contains 3
        # dicts, one for the icon, one for the name (on which is searched), and
        # another one for the checkbox. The parent dict of these 3 contains the
        # index of the button that needs to be clicked.
        item_dict = get_torified_item_index_dict(
            required_object, unpacked_screen_dict, {}
        )
        item_index = int(item_dict["@index"])

        # Click those buttons if they are not enabled.
        if not orbot_torifying_app_is_checked(item_dict):
            dev(index=item_index).click()

    # Refresh the screen.
    dev(descriptionMatches="Refresh Apps").click()

    # Click back.
    dev(descriptionContains="Navigate up").click()

    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
