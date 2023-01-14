"""Completes the tasks specified in the arg_parser."""
import argparse
from pprint import pprint
from typing import Dict, Union

from typeguard import typechecked
from uiautomator import device

from src.appcommander.hardcoded import app_name_mappings
from src.appcommander.helper import export_screen_data, get_screen_as_dict
from src.appcommander.plot_script_flow import visualise_script_flow
from src.appcommander.run_script import run_script
from src.appcommander.Script import Script
from src.appcommander.verification.arg_verification import (
    get_verified_apps_to_torify,
    sort_out_app_name_and_package_name,
)
from src.appcommander.verification.verify_phone_connection import (
    assert_app_is_installed,
    assert_app_version_is_correct,
)


@typechecked
def process_args(args: argparse.Namespace) -> None:
    """Processes the arguments and ensures the accompanying tasks are
    executed."""
    app_name, package_name = sort_out_app_name_and_package_name(
        args.app_name, app_name_mappings=app_name_mappings
    )

    if args.torify:
        torifying_apps: Union[
            Dict[str, str], None
        ] = get_verified_apps_to_torify(app_name_mappings, args.torify)
    else:
        torifying_apps = None

    # Also verifies phone is connected.
    assert_app_is_installed(package_name=package_name)
    assert_app_version_is_correct(
        package_name=package_name,
        app_version=args.version,
    )

    apk_script = Script(
        app_name=app_name,
        overwrite=False,
        package_name=package_name,
        torifying_apps=torifying_apps,
        version=args.version,
    )
    if args.export_screen:
        unpacked_screen_dict: Dict = get_screen_as_dict(
            dev=device,
            unpack=True,
            screen_dict={},
            reload=False,
        )
        export_screen_data(
            dev=device,
            screen_dict=unpacked_screen_dict,
            screen_nr=args.export_screen,
            script=apk_script,
            overwrite=True,
            subdir="unverified",
        )
    elif args.export_script_flow:
        visualise_script_flow(
            G=apk_script.script_graph,
            app_name=apk_script.app_name.replace(".", "_"),
            app_version=apk_script.version.replace(".", "_").replace(" ", "_"),
        )
    else:
        print("")
        pprint(apk_script.__dict__)
        run_script(apk_script, device)
