"""Parses CLI arguments that specify on which platform to simulate the spiking
neural network (SNN)."""
import argparse

from typeguard import typechecked


@typechecked
def parse_cli_args() -> argparse.Namespace:
    """Reads command line arguments and converts them into python arguments."""
    # Instantiate the parser
    parser = argparse.ArgumentParser(
        description="Optional description for arg" + " parser"
    )

    # Create argument parsers to allow user to specify what to run.
    # Allow user run the experiment on a graph from file.
    parser.add_argument(
        "-a",
        "--app-name",
        action="store",
        type=str,
        help=(
            "The name of the Android app as used by your file system. E.g. "
            + "instead of 'Orbot' write: 'org.torproject.android'."
        ),
    )

    # Take a screenshot and store the UI information in a .json file.
    parser.add_argument(
        "-e",
        "--export-screen",
        action="store",
        type=str,
        help=(
            "Specify the screen number whose json data and .png data are "
            + "stored."
        ),
    )

    # Run experiment on a particular experiment_settings json file.
    parser.add_argument(
        "-v",
        "--version",
        action="store",
        type=str,
        help=("Give the version of the Android app."),
    )

    # Load the arguments that are given.
    args = parser.parse_args()
    return args
