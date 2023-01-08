"""Starts a script to control an app."""

from typeguard import typechecked

from src.apkcontroller.scripts.org_torproject_android.v16_6_3_RC_1 import (
    Apk_script,
)


@typechecked
def run_script(script: Apk_script) -> None:
    """Runs the incoming script on the phone."""
    # Script folder structure:
    # app_scripts/app_name/version

    # Open the app.
    # next_screens = get start_screens()
    # get_current_screen.
    # verify current_screen in next_screens.

    # end_screens = get end_screens()

    # while current_screen not in end_screens:
    # if current_screen in next_screens(s):

    # next_screens = get_next_screen(s)(
    # current_screen_name
    # script_graph
    # actions

    # goto_next_screen(
    #   actions
    #   next_screen_index
    print(f"TODO: run script:{script}")
