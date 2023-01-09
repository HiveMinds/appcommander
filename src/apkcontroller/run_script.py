"""Starts a script to control an app."""


from typing import Dict

from typeguard import typechecked
from uiautomator import device

from src.apkcontroller.helper import launch_app
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
    Apk_script,
)
from src.apkcontroller.script_helper import get_current_screen, get_start_nodes


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
    print(f"start_screennames={start_screennames}")

    # get current screen.
    screen_dict: Dict = get_current_screen(device)
    print(screen_dict)

    # verify current_screen in next_screens.

    # end_screens = get end_screens()

    # while current_screen not in end_screens:
    # if current_screen in next_screens(s):

    # next_screens = get_next_screen(s)(
    # current_screen_nr
    # script_graph
    # actions

    # goto_next_screen(
    #   actions
    #   next_screen_index
    print(f"TODO: run script:{script}")
