"""Verifies the given CLI arguments are valid in combination with each
other."""
import argparse
import os
from typing import Dict, List, Tuple

from typeguard import typechecked

from src.apkcontroller.helper import file_exists, make_path_if_not_exists
from src.apkcontroller.verification.verify_phone_connection import (
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
        # TODO: verify all supported package names are unique.

        # app_name = list(app_name_mappings.values()).index(some_apk_name)
        app_name = str(
            {
                i
                for i in app_name_mappings
                if app_name_mappings[i] == some_apk_name
            }
        )
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
        f'src/apkcontroller/{args.app_name.replace(".","_").replace(" ","_")}'
    )
    # User just wants to store screenshots and json, make dirs for user.
    if args.export_screen is not None:
        # TODO: verify app is installed.
        # TODO: verify app version.
        # TODO: create directories if not yet existent.
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
        f'src/apkcontroller/{args.app_name.replace(".","_").replace(" ","_")}/'
        + f'V{args.version.replace(".","_").replace(" ","_")}'
    )
    # User just wants to store screenshots and json, make dirs for user.
    if args.export_screen is not None:
        # TODO: verify app is installed.
        # TODO: verify app version.
        # TODO: create directories if not yet existent.
        make_path_if_not_exists(version_path)
    else:  # User tries to use app name even though app name may not exist.
        if not os.path.exists(version_path):
            raise NotADirectoryError(
                f"Error, path:{version_path} does not exist. "
                + " Please create it and add an accompanying script."
            )
        script_path = f"{version_path}/script.py"
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
    if not file_exists(script_path):
        raise FileNotFoundError(f"Input Graph path was invalid:{script_path}")

    # TODO: Verify script path is valid.


def get_verified_apps_to_torify(
    app_name_mappings: Dict[str, str], torifying_aps_csv: str
) -> List[str]:
    """Converts the comma separated values (csv) of the app names that are to
    be torrified, into a list of app names, and then verifies they are
    installed on the phone."""

    torifying_apps: List[str] = torifying_aps_csv.split(",")
    for app_name in torifying_apps:
        _, package_name = sort_out_app_name_and_package_name(
            app_name, app_name_mappings=app_name_mappings
        )
        assert_app_is_installed(
            package_name=package_name, app_name_mappings=app_name_mappings
        )

    return torifying_apps
