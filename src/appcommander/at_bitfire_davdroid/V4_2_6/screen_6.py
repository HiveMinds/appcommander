"""After the "Connection Request" has been granted, the app welcomes the user
with screens 1,2,3,4."""
# pylint: disable=R0801
import inspect
from typing import TYPE_CHECKING, Callable, Dict, List, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

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

    max_retries = 1
    screen_nr = 6
    wait_time_sec = 1
    required_objects: List[Dict[str, str]] = [
        {
            "@text": "Create account",
        },
        {
            "@text": "Add account",
        },
        {
            "@resource-id": "at.bitfire.davdroid:id/accountName",
        },
        {
            "@text": "CREATE ACCOUNT",
        },
        {
            "@text": (
                "Use your email address as account name because Android will "
                + "use the account name as ORGANIZER field for events you "
                + "create. You can't have two accounts with the same name."
            ),
        },
    ]

    # pylint: disable=W0613
    @typechecked
    def get_next_actions(
        required_objects: List[Dict[str, str]],
        optional_objects: List[Dict[str, str]],
        script: Script,
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
        get_next_actions=get_next_actions,
        is_start=True,
        max_retries=max_retries,
        screen_nr=screen_nr,
        wait_time_sec=wait_time_sec,
        required_objects=required_objects,
    )


# pylint: disable=W0613
@typechecked
def actions_0(dev: AutomatorDevice, screen: Screen, script: Script) -> Dict:
    """Performs the actions in option 0 in this screen.

    For this screen, it waits until the phone is done querying the
    server.
    """
    dev(resourceId="at.bitfire.davdroid:id/accountName").set_text(
        script.input_data.nextcloud_username
    )

    # Press CREATE ACCOUNT button.
    dev(resourceId="at.bitfire.davdroid:id/create_account").click()
    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])  # 8 for:len(actions__)
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
