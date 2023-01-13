"""Starts a script to control an app."""


from typing import Dict, List

from typeguard import typechecked
from uiautomator import device

from src.apkcontroller.helper import export_screen_data_if_valid, launch_app
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.screen_flow import (
    visualise_script_flow,
)
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
    visualise_script_flow(
        G=script.script_graph,
        app_name=script.script_description["app_name"].replace(".", "_"),
        app_version=script.script_description["version"]
        .replace(".", "_")
        .replace(" ", "_"),
    )

    # Open the app.
    app_name = script.script_description["app_name"]
    launch_app(app_name)

    expected_screens: List[int] = get_start_nodes(script.script_graph)

    _, screen_nr = can_proceed(
        device=device,
        expected_screennames=expected_screens,
        retry=True,
        script=script,
    )
    script.script_description["past_screens"] = [screen_nr]

    next_actions = "filler"
    retry: bool = False  # For the first screen, do a quick scope because it is
    # known already.
    while next_actions is not None:
        _, screen_nr = can_proceed(
            device=device,
            expected_screennames=expected_screens,
            retry=retry,
            script=script,
        )
        retry = True
        screen = script.script_graph.nodes[screen_nr]["Screen"]
        print(f"screen_nr={screen_nr}")

        # Export the data of the screens if they happen to be found in the
        # device already.
        export_screen_data_if_valid(
            device=device,
            overwrite=script.script_description["overwrite"],
            screens=[screen],
        )

        # Get next action
        next_actions = screen.get_next_actions(
            required_objects=screen.required_objects,
            optional_objects=screen.optional_objects,
            history=script.script_description,
        )

        # Perform next action.
        if next_actions is not None:

            # Compose the information needed for the actions.
            additional_info = script.script_description
            additional_info["screen_nr"] = screen_nr
            additional_info["script_graph"] = script.script_graph

            # Perform the actual action.
            action_output: Dict = script.perform_action(
                device=device,
                next_actions=next_actions,
                additional_info=additional_info,
            )
            expected_screens = action_output["expected_screens"]
            script.script_description["past_screens"].append(screen_nr)

    print(f'Done with script:{script.script_description["app_name"]}')
