"""Verifies the given CLI arguments are valid in combination with each
other."""
import argparse

from typeguard import typechecked

from src.apkcontroller.helper import file_exists


@typechecked
def verify_args(args: argparse.Namespace) -> None:
    """Performs the checks to verify the parser."""
    if isinstance(args.script_path, str):
        verify_app_script(args.script_path)


@typechecked
def verify_app_script(script_path: str) -> None:
    """Verifies the filepath for the input graph exists and contains a valid
    networkx graph."""
    # Assert graph file exists.
    if not file_exists(script_path):
        raise FileNotFoundError(f"Input Graph path was invalid:{script_path}")

    # TODO: Verify script path is valid.
