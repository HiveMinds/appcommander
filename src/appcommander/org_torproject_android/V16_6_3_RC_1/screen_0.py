"""First entry point on app if it is freshly installed.

Presents a: "Connection Request".
"""
# pylint: disable=R0801
import inspect
from typing import TYPE_CHECKING, Callable, Dict, List, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.appcommander.Screen import Screen
from src.appcommander.script_orientation import get_expected_screen_nrs

if TYPE_CHECKING:
    from src.appcommander.Script import Script
else:
    Script = object


@typechecked
def screen_0() -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""
    max_retries = 5
    screen_nr = 0
    wait_time_sec = 1
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
        # In the start screen just press ok.
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
    """Performs the actions in option 1 in this screen.

    For this screen, it clicks the "OK" button in the "Connection
    request".
    """
    # Click the ok button.
    dev(resourceId="android:id/button1").click()

    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
