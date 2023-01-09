"""Verifies the given CLI arguments are valid in combination with each
other."""
import argparse
import os

from typeguard import typechecked

from src.apkcontroller.helper import file_exists, make_path_if_not_exists


@typechecked
def verify_args(args: argparse.Namespace) -> None:
    """Performs the checks to verify the parser."""
    verify_app_name(args)
    verify_app_version(args)

    if isinstance(args.script_path, str):
        verify_app_script(args.script_path)


@typechecked
def verify_app_name(args: argparse.Namespace) -> None:
    """Verifies the app name is specified and that its folder exists, unless
    the user only wants to store screenshots, in that case, the app name and
    version can be create automatically."""
    # Verify the app name is specified.
    if args.app_name is None:
        raise NameError("Error, app name is not specified.")

    app_path: str = f'src/apkcontroller/{args.app_name.replace(".","_")}'
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
        f'src/apkcontroller/{args.app_name.replace(".","_")}/'
        + f'{args.version.replace(".","_")}'
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


@typechecked
def verify_app_script(script_path: str) -> None:
    """Verifies the filepath for the input graph exists and contains a valid
    networkx graph."""

    # Assert graph file exists.
    if not file_exists(script_path):
        raise FileNotFoundError(f"Input Graph path was invalid:{script_path}")

    # TODO: Verify script path is valid.
