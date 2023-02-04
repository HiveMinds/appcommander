"""Starts a script to control an app."""


from typing import Callable, Dict, List

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.appcommander.helper import export_screen_data_if_valid
from src.appcommander.Screen import Screen
from src.appcommander.Script import Script
from src.appcommander.verification.status_verification import can_proceed


@typechecked
def run_script(script: Script, dev: AutomatorDevice) -> None:
    """Runs the incoming script on the phone.

    Script folder structure: src/appcommander/app_name/version.py with
    app_name is something like: com_whatsapp_android (not: Whatsapp). It
    is derived from how your android dev calls the app, with the dots
    replaced by underscores. E.g. com.whatsapp.android or something like
    that.
    """

    # Open the app.
    # script.input_data.launch_app(app_name=script.app_name)
    script.input_data.launch_app(package_name=script.package_name)

    expected_screens: List[int] = list(
        map(lambda x: x.screen_nr, script.screens)
    )

    # First perorm a quick scope, without retry to find the desired screen.
    is_expected, screen_nr = can_proceed(
        dev=dev,
        expected_screennames=expected_screens,
        retry=False,
        script=script,
    )

    # If quickscope did not find desired screen, try again with retries and
    # waiting times per retry.
    if not is_expected:
        _, screen_nr = can_proceed(
            dev=dev,
            expected_screennames=expected_screens,
            retry=True,
            script=script,
        )
    script.past_screens.append(screen_nr)

    next_actions = "filler"
    retry: bool = False  # For the first screen, do a quick scope because it is
    # known already.
    while next_actions is not None and expected_screens:
        _, screen_nr = can_proceed(
            dev=dev,
            expected_screennames=expected_screens,
            retry=retry,
            script=script,
        )
        retry = True
        screen = script.script_graph.nodes[screen_nr]["Screen"]
        print(f"screen_nr={screen_nr}")

        # Export the data of the screens if they happen to be found in the
        # dev already.
        export_screen_data_if_valid(
            dev=dev,
            overwrite=script.overwrite,
            screens=[screen],
            script=script,
        )

        # Get next action
        next_actions = screen.get_next_actions(
            required_objects=screen.required_objects,
            optional_objects=screen.optional_objects,
            script=script,
        )

        # Perform next action.
        if next_actions is not None:

            # Compose the information needed for the actions.

            # Perform the actual action.
            action_output: Dict = perform_action(
                dev=dev,
                next_actions=next_actions,
                screen=screen,
                script=script,
            )
            expected_screens = action_output["expected_screens"]
            script.past_screens.append(screen_nr)

    print(f"Done with script:{script.app_name}")


@typechecked
def perform_action(
    dev: AutomatorDevice,
    next_actions: Callable,
    screen: Screen,
    script: Script,
) -> Dict:
    """Performs the first action list in the list of action lists."""
    action_output: Dict = next_actions(
        dev=dev,
        screen=screen,
        script=script,
    )
    if "expected_screens" not in action_output.keys():
        raise KeyError(
            "Error, the action output did not contain the expected screens."
        )
    return action_output
