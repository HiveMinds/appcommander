"""Completes the tasks specified in the arg_parser."""
import argparse
from typing import Dict

from typeguard import typechecked
from uiautomator import device

from src.apkcontroller.hardcoded import app_name_mappings
from src.apkcontroller.helper import export_screen_data, get_screen_as_dict
from src.apkcontroller.org_torproject_android.V16_6_3_RC_1.script import (
    Apk_script,
)
from src.apkcontroller.run_script import run_script
from src.apkcontroller.verification.arg_verification import (
    get_verified_apps_to_torify,
    sort_out_app_name_and_package_name,
)
from src.apkcontroller.verification.verify_phone_connection import (
    assert_app_is_installed,
    assert_app_version_is_correct,
)


@typechecked
def process_args(args: argparse.Namespace) -> None:
    """Processes the arguments and ensures the accompanying tasks are
    executed."""
    _, package_name = sort_out_app_name_and_package_name(
        args.app_name, app_name_mappings=app_name_mappings
    )

    if args.torify:
        torifying_apps: Dict[str, str] = get_verified_apps_to_torify(
            app_name_mappings, args.torify
        )

    # Also verifies phone is connected.
    assert_app_is_installed(package_name=package_name)
    assert_app_version_is_correct(
        package_name=package_name,
        app_version=args.version,
    )

    if args.export_screen:
        screen_dict = get_screen_as_dict(device)
        script_description: Dict = {
            "app_name": package_name,
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
        apk_script = Apk_script(torifying_apps=torifying_apps)
        # TODO: only if device is connected pass device.
        # apk_script = Apk_script(device=device)

        print("")
        run_script(apk_script)
    print("DONE")
