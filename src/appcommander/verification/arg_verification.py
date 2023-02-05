"""Verifies the given CLI arguments are valid in combination with each
other."""
import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple

from typeguard import typechecked

from appcommander.helper import make_path_if_not_exists
from appcommander.verification.verify_phone_connection import (
    assert_app_is_installed,
)


@typechecked
def sort_out_app_name_and_package_name(
    some_apk_name: str, app_name_mappings: Dict[str, str]
) -> Tuple[str, str]:
    """Returns app name and package name based on user input and supported apk
    packages."""

    if some_apk_name in app_name_mappings.keys():
        app_name = some_apk_name
        package_name = app_name_mappings[app_name]
    elif some_apk_name in app_name_mappings.values():
        for key in app_name_mappings.keys():
            if app_name_mappings[key] == some_apk_name:
                app_name = key
        package_name = some_apk_name
    return app_name, package_name


@typechecked
def verify_args(args: argparse.Namespace) -> None:
    """Performs the checks to verify the parser."""
    verify_app_name(args)
    verify_app_version(args)


@typechecked
def verify_app_name(args: argparse.Namespace) -> None:
    """Verifies the app name is specified and that its folder exists, unless
    the user only wants to store screenshots, in that case, the app name and
    version can be create automatically."""
    # Verify the app name is specified.
    if args.app_name is None:
        raise NameError("Error, app name is not specified.")

    app_path: str = (
        f'src/appcommander/{args.app_name.replace(".","_").replace(" ","_")}'
    )
    # User just wants to store screenshots and json, make dirs for user.
    if args.export_screen is not None:
        make_path_if_not_exists(app_path)
    else:  # User tries to use app name even though app name may not exist.
        if not os.path.exists(app_path):
            raise NotADirectoryError(
                f"Error, path:{app_path} does not exist. Please create it."
            )


@typechecked
def verify_app_version(args: argparse.Namespace) -> None:
    """Verifies the app version is specified and that its folder exists, unless
    the user only wants to store screenshots, in that case, the app version can
    be create automatically."""
    # Verify the app name is specified.
    if args.version is None:
        raise NameError("Error, app version is not specified.")

    version_path: str = (
        f'src/appcommander/{args.app_name.replace(".","_").replace(" ","_")}/'
        + f'V{args.version.replace(".","_").replace(" ","_")}'
    )
    # User just wants to store screenshots and json, make dirs for user.
    if args.export_screen is not None:
        # Create directories if not yet existent.
        make_path_if_not_exists(version_path)
    else:  # User tries to use app name even though app name may not exist.
        if not os.path.exists(version_path):
            raise NotADirectoryError(
                f"Error, path:{version_path} does not exist. "
                + " Please create it and add an accompanying script."
            )
        script_path = f"{version_path}/Screen_flow.py"
        if not os.path.exists(script_path):
            raise NotADirectoryError(
                f"Error, path:{script_path} does not exist. "
                + " Please create it and make it work."
            )


@typechecked
def verify_app_script(script_path: str) -> None:
    """Verifies the filepath for the input graph exists and contains a valid
    networkx graph."""

    # Assert graph file exists.
    if not Path(script_path).is_file():
        raise FileNotFoundError(f"Input Graph path was invalid:{script_path}")


def get_verified_apps_to_torify(
    app_name_mappings: Dict[str, str], torifying_aps_csv: str
) -> Dict[str, str]:
    """Converts the comma separated values (csv) of the app names that are to
    be torified, into a list of app names, and then verifies they are installed
    on the phone."""

    some_apps: List[str] = torifying_aps_csv.split(",")
    torryfying_apps: Dict[str, str] = {}
    for app_name in some_apps:
        app_name, package_name = sort_out_app_name_and_package_name(
            app_name, app_name_mappings=app_name_mappings
        )
        assert_app_is_installed(
            package_name=package_name,
        )
        torryfying_apps[app_name] = package_name

    return torryfying_apps
