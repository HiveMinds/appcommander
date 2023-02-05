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
def screen_3() -> Screen:
    """Creates the settings for a starting screen where Orbot is not yet
    started."""

    max_retries = 1
    screen_nr = 3
    wait_time_sec = 1
    required_objects: List[Dict[str, str]] = [
        {
            # Original:
            # "@text":
            # "DAVx\u2075 has encountered an unknown
            # certificate. Do you want to trust it?",
            "@text": (
                "has encountered an unknown certificate. Do you want to "
                + "trust it?"
            ),
        },
        {
            "@text": "X509 certificate details",
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

    For this screen, it clicks the "Next" button (icon=">") in the
    bottom right.
    """

    dev(text="I have manually verified the whole fingerprint.").click()
    dev(text="ACCEPT").click()

    print(
        "TODO: (re-enable) The root CA (your self-signed certificate) that "
        + "was created for "
        + "your Nextcloud server has not yet been installed on your phone. "
        + "Doing that now for you."
    )
    # install_self_signed_root_ca_on_android(
    #    script.app_version_dir,
    # )

    # Open the app again.
    script.input_data.launch_app(package_name=script.package_name)

    # Return the expected screens, using get_expected_screen_nrs.
    action_nr: int = int(inspect.stack()[0][3][8:])
    screen_nr: int = screen.screen_nr
    script_flow: nx.DiGraph = script.script_graph
    return {
        "expected_screens": get_expected_screen_nrs(
            G=script_flow, screen_nr=screen_nr, action_nr=action_nr
        )
    }
