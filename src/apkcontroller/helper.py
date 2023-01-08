"""Contains helper functions that are used throughout this repository."""
import json
import os
import subprocess  # nosec
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Union

import xmltodict
from typeguard import typechecked
from uiautomator import AutomatorDevice

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
def get_screen_as_dict(device: AutomatorDevice) -> Dict:
    """Loads the phone and shows the screen as a dict.

    from uiautomator import device as d
    """
    doc = xmltodict.parse(device.dump())
    return doc


@typechecked
def required_objects_in_screen(
    required_objects: List[Dict[str, Union[List, Dict, str]]],
    screen: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all required objects are found in the UI/screen.

    False otherwise.
    """
    for required_object in required_objects:
        if not required_object_in_screen(required_object, screen):
            return False
    return True


@typechecked
def required_object_in_screen(
    required_object: Dict[str, Union[List, Dict, str]],
    screen: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all the keys and values in a dict are found within the
    same key or list of the xml of the ui."""
    if dict_contains_other_dict(required_object, screen):
        return True
    if "node" in screen.keys():
        if isinstance(screen["node"], Dict):
            if required_object_in_screen(required_object, screen["node"]):
                return True
        if isinstance(screen["node"], List):
            for node_elem in screen["node"]:
                if required_object_in_screen(required_object, node_elem):
                    return True
    return False


@typechecked
def dict_contains_other_dict(sub: Dict, main: Dict) -> bool:
    """Returns true if the sub dict is a subset of the main dict."""
    for sub_key, sub_val in sub.items():
        if sub_key not in main.keys():
            return False
        if sub_val != main[sub_key]:
            return False
    return True


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
    screen_objects: List[Screen],
) -> None:
    """Checks whether the required objects are in the actual screen, and if
    they are, it exports the data of the screen in json format and as a
    screenshot."""
    if device is not None:
        for screen in screen_objects:
            if screen.is_expected_screen(device=device):
                screen.export_screen_data(device=device, overwrite=overwrite)


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
        await_compilation=True, bash_command=command, verbose=True
    )

    # TODO: verify app is laucned
