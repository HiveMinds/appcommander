"""Can be first screen after "Connection request" has been satisfied. The tor-
bridge is not yet started.

Presents a: "Connection request".
"""
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
def screen_5() -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""

    max_retries = 5
    screen_nr = 5
    wait_time_sec = 1
    required_objects: List[Dict[str, str]] = [
        {
            "@text": "Global " "(Auto)",
        },
        {
            "@text": "Trouble " "connecting?",
        },
        {
            "@text": "Use Bridges",
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
        if 6 in script.past_screens:
            # run start.
            return actions_1
        # Else:
        # Go to settings, and enable the required apps.
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
    """Go to settings inside Orbot to select which apps are torified."""

    # Click in the screen to go to the Orbot settings on which app to torify.
    dev(resourceId="org.torproject.android:id/ivAppVpnSettings").click()

    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }


# pylint: disable=W0613
@typechecked
def actions_1(dev: AutomatorDevice, screen: Screen, script: Script) -> Dict:
    """Click the start tor bridge button in the Orbot app main screen."""

    # Press the START button in the Orbot app to create a tor connection.
    dev(resourceId="org.torproject.android:id/imgStatus").click()

    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
