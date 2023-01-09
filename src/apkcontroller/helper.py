"""Contains helper functions that are used throughout this repository."""
import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.script_helper import (
    get_screen_as_dict,
    is_expected_screen,
)

if TYPE_CHECKING:
    from src.apkcontroller.Screen import Screen
else:
    Screen = object


@typechecked
def file_exists(filepath: str) -> bool:
    """Checks if file exists.

    :param string:
    """
    # TODO: Execute Path(string).is_file() directly instead of calling this
    # function.
    my_file = Path(filepath)
    return my_file.is_file()


@typechecked
def output_json(output_dir: str, filename: str, screen_dict: Dict) -> None:
    """Outputs a json to a filepath, ensures the output dir exists, overwrites
    json if it already exists."""

    make_path_if_not_exists(output_dir)

    output_path = f"{output_dir}{filename}"
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(screen_dict, fp, indent=4, sort_keys=True)
        fp.close()

    # Verify the file exists.
    if not Path(output_path).is_file():
        raise Exception(f"Error, filepath:{output_path} was not created.")


@typechecked
def load_json_file_into_dict(
    json_filepath: str,
) -> Dict:
    """Loads a json file into dict from a filepath."""
    if not Path(json_filepath).is_file():
        raise Exception("Error, filepath does not exist:{filepath}")
    # TODO: verify extension.
    # TODO: verify json formatting is valid.
    with open(json_filepath, encoding="utf-8") as json_file:
        the_dict = json.load(json_file)
        json_file.close()
    return the_dict


@typechecked
def make_path_if_not_exists(path: str) -> None:
    """Creates a filepath if it does not yet exist."""
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path):
        raise Exception(f"Error, path:{path} did not exist after creation.")


@typechecked
def export_screen_data_if_valid(
    device: AutomatorDevice,
    overwrite: bool,
    screens: List[Screen],
) -> None:
    """Checks whether the required objects are in the actual screen, and if
    they are, it exports the data of the screen in json format and as a
    screenshot."""
    if device is not None:
        for screen in screens:
            if screen.screen_dict is None:
                # Load and unpack the screen dict to get meaningful ui info.
                screen.screen_dict = get_screen_as_dict(device)
            unpacked_screen_dict = screen.screen_dict["hierarchy"]
            if is_expected_screen(
                unpacked_screen_dict=unpacked_screen_dict,
                expected_screen=screen,
            ):
                export_screen_data(
                    device=device,
                    screen_dict=screen.screen_dict,
                    script_description=screen.script_description,
                    overwrite=overwrite,
                    unverified=False,
                )


@typechecked
def run_bash_command(
    await_compilation: bool, bash_command: str, verbose: bool
) -> None:
    """Runs a bash command."""
    if await_compilation:
        if verbose:
            subprocess.call(bash_command, shell=True)  # nosec
        else:
            subprocess.call(  # nosec
                bash_command,
                shell=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
    else:
        if verbose:
            # pylint: disable=R1732
            subprocess.Popen(bash_command, shell=True)  # nosec
        else:
            # pylint: disable=R1732
            subprocess.Popen(  # nosec
                bash_command,
                shell=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )


@typechecked
def launch_app(app_name: str) -> None:
    """Launches app on phone."""

    # TODO: verify phone is connected.

    # Launc the app on phone.
    command = f'adb shell monkey -p "{app_name}" 1 &>/dev/null'
    run_bash_command(
        await_compilation=True, bash_command=command, verbose=False
    )

    # TODO: verify app is laucned


@typechecked
def export_screen_data(
    device: AutomatorDevice,
    screen_dict: Dict,
    script_description: Dict[str, str],
    overwrite: bool = False,
    unverified: bool = True,
) -> None:
    """Writes a dict file to a .json file, and exports a screenshot.

    The overwrite bool determines whether a file will be overwritten or
    not if it  already exists. The unverified bool determines whether
    the screen data is verified to be expected, or not. If not, the
    screen data is placed in a subfolder named: unverified, to reduce
    the probability of the developer basing script actions on data
    belonging to the wrong screen.
    """
    if unverified:
        unverified_dir = "unverified/"
    else:
        unverified_dir = ""
    output_dir = (
        (
            "src/apkcontroller/"
            + f'{script_description["app_name"]}'
            + f'/V{script_description["version"]}/{unverified_dir}'
        )
        .replace(".", "_")
        .replace(" ", "_")
    )
    output_name = f'{script_description["screen_nr"]}'

    for extension in [".json", ".png"]:
        output_path = f"{output_dir}{output_name}{extension}"
        if not Path(output_path).is_file() or overwrite:

            if extension == ".json":
                if screen_dict is None:
                    screen_dict = get_screen_as_dict(device)
                output_json(output_dir, f"{output_name}.json", screen_dict)
            if extension == ".png":
                # device.takeScreenshot(output_path)
                device.screenshot(output_path)

        # Verify the file exists.
        if not Path(output_path).is_file():
            raise Exception(f"Error, filepath:{output_path} was not created.")
