"""Completes the tasks specified in the arg_parser."""
import argparse
from typing import Dict, Union

from typeguard import typechecked
from uiautomator import device

from src.apkcontroller.helper import export_screen_data, get_screen_as_dict
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
    Apk_script,
)
from src.apkcontroller.run_script import run_script
from src.apkcontroller.verification.verify_phone_connection import (
    assert_app_is_installed,
    assert_app_version_is_correct,
)


@typechecked
def process_args(args: argparse.Namespace) -> None:
    """Processes the arguments and ensures the accompanying tasks are
    executed."""

    # Also verifies phone is connected.
    assert_app_is_installed(args.app_name)
    assert_app_version_is_correct(args.version)

    if args.export_screen:
        screen_dict = get_screen_as_dict(device)
        script_description: Dict[str, Union[bool, int, str]] = {
            "app_name": args.app_name,
            "version": args.version,
            "screen_nr": args.export_screen,
        }
        export_screen_data(
            device=device,
            screen_dict=screen_dict,
            script_description=script_description,
            overwrite=True,
            unverified=True,
        )
    else:
        apk_script = Apk_script()
        # TODO: only if device is connected pass device.
        # apk_script = Apk_script(device=device)

        print("")
        run_script(apk_script)
    print("DONE")
