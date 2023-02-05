"""TODO Documentation."""
# pylint: disable=R0801
from typing import TYPE_CHECKING, Callable, Dict, List, Union

from typeguard import typechecked
from uiautomator import AutomatorDevice

from appcommander.Screen import Screen

if TYPE_CHECKING:
    from appcommander.Script import Script
else:
    Script = object


@typechecked
def screen_2() -> Screen:
    """Creates the settings for when DAVx5 is querying the Nextcloud
    server.."""
    max_retries = 5
    screen_nr = 2
    wait_time_sec = 1
    required_objects: List[Dict[str, str]] = [
        {
            "@package": "at.bitfire.davdroid",
        },
        {
            "@text": "Couldn't find CalDAV or CardDAV service.",
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
    # TODO: Was not able to connect to tor. Restart orbot and try again.
    raise Exception(
        "Error, was not able to connect to TOR server, please:"
        + " Ensure your Nextcloud server is running and reachable over tor,"
        + " and ensure Orbot is torifying DAVx5, and connected to TOR."
    )
