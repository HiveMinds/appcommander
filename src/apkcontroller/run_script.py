"""Starts a script to control an app."""


import time
from typing import Callable, Dict, List

from typeguard import typechecked
from uiautomator import AutomatorDevice, device

from src.apkcontroller.helper import launch_app
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
    Apk_script,
)
from src.apkcontroller.script_helper import (
    can_proceed,
    get_end_nodes,
    get_start_nodes,
)


@typechecked
def run_script(script: Apk_script) -> None:
    """Runs the incoming script on the phone.

    Script folder structure: src/apkcontroller/app_name/version.py with
    app_name is something like: com_whatsapp_android (not: Whatsapp). It
    is derived from how your android device calls the app, with the dots
    replaced by underscores. E.g. com.whatsapp.android or something like
    that.
    """

    # Open the app.
    app_name = script.script_description["app_name"]
    launch_app(app_name)

    start_screennames = get_start_nodes(script.script_graph)
    end_screennames = get_end_nodes(script.script_graph)
    print(f"start_screennames={start_screennames}")

    _, screen_nr = can_proceed(
        device=device, expected_screennames=start_screennames, script=script
    )

    print(f"end_nodes={end_screennames}")
    print(f"screen_nr={screen_nr}")
    while screen_nr not in end_screennames:
        _, screen_nr = can_proceed(
            device=device,
            expected_screennames=start_screennames,
            script=script,
        )
        print(f"screen_nr={screen_nr}")
        time.sleep(1)

        # Get next action
        screen = script.script_graph.nodes[screen_nr]["Screen"]
        next_actions: List[
            Callable[
                [Dict[str, str], Dict[str, str], Dict[str, str]],
                List[Callable[[AutomatorDevice], None]],
            ]
        ] = screen.get_next_actions(
            required_objects=screen.required_objects,
            optional_objects=screen.optional_objects,
            history={},
        )
        # Perform next action.
        if len(next_actions) == 0:
            raise ValueError("No action functions was returned.")
        if len(next_actions) > 1:
            raise ValueError("More than one action functions were returned.")

        next_actions[0](device=device)  # type: ignore[call-arg]

        # next_screens = get_next_screen(s)(
        # current_screen_nr
        # script_graph
        # actions

        # goto_next_screen(
        #   actions
        #   next_screen_index
    print("DONE")
