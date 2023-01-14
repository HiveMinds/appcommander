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
        type=int,
        help=(
            "Specify the screen number whose json data and .png data are "
            + "stored."
        ),
    )

    # Take a screenshot and store the UI information in a .json file.
    parser.add_argument(
        "-f",
        "--export_script_flow",
        action="store_true",
        help=("Show a graph  of the screen flow of this script for an app."),
    )

    # Create argument to allow user to specify which apps Orbot should torify.
    parser.add_argument(
        "-t",
        "--torify",
        action="store",
        type=str,
        help=(
            "The names (csv) of the Android apps that you want Orbot to torify"
            + ". You can choose from (left or right):'."
        ),
    )

    # Create argument to allow user to specify its nextcloud username.
    parser.add_argument(
        "-nu",
        "--nextcloud-username",
        action="store",
        type=str,
        help=("Your Nextcloud username."),
    )

    # Create argument to allow user to specify its nextcloud username.
    parser.add_argument(
        "-np",
        "--nextcloud-password",
        action="store",
        type=str,
        help=(
            "Your Nextcloud password. "
            + "TODO: build support for local safe passing."
        ),
    )

    # Create argument to allow user to specify your onion url.
    parser.add_argument(
        "-o",
        "--onion-url",
        action="store",
        type=str,
        help=("Your url like: lakjdsf2340usdffa.onion"),
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
