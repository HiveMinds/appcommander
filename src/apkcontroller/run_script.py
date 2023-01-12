"""Starts a script to control an app."""


import time
from typing import Dict, List

from typeguard import typechecked
from uiautomator import device

from src.apkcontroller.helper import launch_app
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
    Apk_script,
)
from src.apkcontroller.script_helper import can_proceed, get_start_nodes


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

    expected_screens: List[int] = get_start_nodes(script.script_graph)

    _, screen_nr = can_proceed(
        device=device, expected_screennames=expected_screens, script=script
    )
    script.script_description["past_screens"] = [screen_nr]

    next_actions = ["filler"]
    while len(next_actions) >= 1:
        time.sleep(1)  # TODO: replace with max_wait and retries of expected
        # screens. and pass to can_proceed.
        _, screen_nr = can_proceed(
            device=device,
            expected_screennames=expected_screens,
            script=script,
        )
        print(f"screen_nr={screen_nr}")

        # Get next action
        screen = script.script_graph.nodes[screen_nr]["Screen"]
        next_actions = screen.get_next_actions(
            required_objects=screen.required_objects,
            optional_objects=screen.optional_objects,
            history=script.script_description,
        )

        # Perform next action.
        if len(next_actions) != 0:
            if len(next_actions) > 1:
                raise ValueError(
                    "More than one action functions were returned."
                )

            action_output: Dict = script.perform_action(
                device=device,
                next_actions=next_actions,
                screen_nr=screen_nr,
                additional_info=script.script_description,
            )
            expected_screens = action_output["expected_screens"]

            script.script_description["past_screens"].append(screen_nr)

    print(f'Done with script:{script.script_description["app_name"]}')
