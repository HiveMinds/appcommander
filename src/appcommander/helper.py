"""Contains helper functions that are used throughout this repository."""
import json
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Union

import xmltodict
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.appcommander.run_bash_code import run_bash_command

if TYPE_CHECKING:
    from src.appcommander.Screen import Screen
    from src.appcommander.Script import Script
else:
    Screen = object
    Script = object


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
        raise Exception(f"Error, filepath does not exist:{json_filepath}")

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
    dev: AutomatorDevice,
    overwrite: bool,
    screens: List[Screen],
    script: Script,
) -> None:
    """Checks whether the required objects are in the actual screen, and if
    they are, it exports the data of the screen in json format and as a
    screenshot."""
    if dev is not None:
        for screen in screens:
            # Load and unpack the screen dict to get meaningful ui info.
            screen.screen_dict = get_screen_as_dict(
                dev=dev,
                unpack=True,
                screen_dict=screen.screen_dict,
                reload=False,
            )

            if is_expected_screen(
                dev=dev,
                unpacked_screen_dict=screen.screen_dict,
                retry=True,
                expected_screen=screen,
            ):
                export_screen_data(
                    dev=dev,
                    screen_dict=screen.screen_dict,
                    screen_nr=screen.screen_nr,
                    script=script,
                    overwrite=overwrite,
                    subdir="verified",
                )


@typechecked
def launch_app(app_name: str) -> None:
    """Launches app on phone."""

    # Launch the app on phone.
    command = f'adb shell monkey -p "{app_name}" 1 &>/dev/null'
    run_bash_command(
        await_compilation=True, bash_command=command, verbose=False
    )


# pylint: disable=R0913
@typechecked
def export_screen_data(
    dev: AutomatorDevice,
    screen_dict: Dict,
    screen_nr: int,
    script: Script,
    overwrite: bool = False,
    subdir: str = "unverified",
) -> None:
    """Writes a dict file to a .json file, and exports a screenshot.

    The overwrite bool determines whether a file will be overwritten or
    not if it  already exists. The subdir bool determines whether the
    screen data is verified to be expected, or not. If not, the screen
    data is placed in a subfolder named: subdir, to reduce the
    probability of the developer basing script actions on data belonging
    to the wrong screen.
    """
    output_dir = (
        (
            "src/appcommander/"
            + f"{script.package_name}"
            + f"/V{script.version}/{subdir}/"
        )
        .replace(".", "_")
        .replace(" ", "_")
    )
    output_name = f"{screen_nr}"

    for extension in [".json", ".png"]:
        output_path = f"{output_dir}{output_name}{extension}"
        if not Path(output_path).is_file() or overwrite:

            if extension == ".json":
                if screen_dict == {}:
                    screen_dict = get_screen_as_dict(
                        dev=dev,
                        unpack=True,
                        screen_dict=screen_dict,
                        reload=False,
                    )
                output_json(output_dir, f"{output_name}.json", screen_dict)
            if extension == ".png":
                # dev.takeScreenshot(output_path)
                dev.screenshot(output_path)

        # Verify the file exists.
        if not Path(output_path).is_file():
            raise Exception(f"Error, filepath:{output_path} was not created.")


@typechecked
def get_screen_as_dict(
    dev: AutomatorDevice,
    unpack: bool,
    screen_dict: Dict,
    reload: bool = False,
) -> Dict:
    """Loads the phone and shows the screen as a dict."""

    # Don't reload if the screen dict still exists, and no explicit
    # reload is asked.
    if screen_dict != {} and not reload:
        if unpack and "hierarchy" in screen_dict.keys():
            return screen_dict["hierarchy"]
        return screen_dict

    # Get the new screen data from the ui.
    if screen_dict == {} or reload:
        print("Loading screen data from phone for orientation.")
        ui_information: Dict = xmltodict.parse(dev.dump())

        # Unpack the screen dict to get a recursive dictionary structure.
        if unpack:
            ui_information = ui_information["hierarchy"]
    return ui_information


@typechecked
def is_expected_screen(
    dev: AutomatorDevice,
    expected_screen: Screen,
    retry: bool,
    unpacked_screen_dict: Dict,
    verbose: Optional[bool] = False,
) -> bool:
    """Custom verification per screen based on the optional and required
    objects in screen.

    Raise error if verification fails.
    """

    # Preliminary check to see if the required objects are in.
    if not required_objects_in_screen(
        expected_screen.required_objects, unpacked_screen_dict
    ):
        if not retry:
            return False
        # Retry and return True if the required objects were found.
        for _ in range(0, expected_screen.max_retries):

            # Reload the screen data again.
            unpacked_screen_dict = get_screen_as_dict(
                dev=dev,
                unpack=True,
                screen_dict={},
                reload=True,
            )
            print(
                f"Wait: {expected_screen.wait_time_sec} [s] on screen: "
                + f"{expected_screen.screen_nr}"
            )
            time.sleep(expected_screen.wait_time_sec)
            if required_objects_in_screen(
                required_objects=expected_screen.required_objects,
                unpacked_screen_dict=unpacked_screen_dict,
            ):
                return True
            if verbose:
                print(f"Not found:{expected_screen.required_objects}")
        if verbose:
            print(f"Not found:{expected_screen.required_objects}")
        return False
    # else:
    return True


@typechecked
def required_objects_in_screen(
    required_objects: List[Dict[str, Union[List, Dict, str]]],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all required objects are found in the UI/screen.

    False otherwise.
    """
    for required_object in required_objects:
        if not required_object_in_screen(
            required_object=required_object,
            unpacked_screen_dict=unpacked_screen_dict,
        ):
            return False
    return True


@typechecked
def required_object_in_screen(
    required_object: Dict[str, Union[List, Dict, str]],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
) -> bool:
    """Returns True if all the keys and values in a dict are found within the
    same key or list of the xml of the ui."""
    if dict_contains_other_dict(required_object, unpacked_screen_dict):
        return True
    if "node" in unpacked_screen_dict.keys():
        if isinstance(unpacked_screen_dict["node"], Dict):
            if required_object_in_screen(
                required_object=required_object,
                unpacked_screen_dict=unpacked_screen_dict["node"],
            ):
                return True
        if isinstance(unpacked_screen_dict["node"], List):
            for node_elem in unpacked_screen_dict["node"]:
                if required_object_in_screen(
                    required_object=required_object,
                    unpacked_screen_dict=node_elem,
                ):
                    return True
        if not isinstance(unpacked_screen_dict["node"], Dict | List):
            raise TypeError("Node value of unexpected type.")
    return False


@typechecked
def dict_contains_other_dict(sub: Dict, main: Dict) -> bool:
    """Returns true if the sub dict is a subset of the main dict."""
    for sub_key, sub_val in sub.items():
        if sub_key not in main.keys():
            return False
        # An artifact like:
        # "@text": "VPN Mode \u200e\u200f\u200e\u200e\u200e\u200e\u200e\u200f
        # \u200e\u200f\u200f\u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\
        # u200e\u200e\u200f\u200e\u200e\u200e\u200e\u200f\u200f\u200f\u200f\
        # u200f\u200e\u200e\u200f\u200f\u200e\u200e\u200e\u200f\u200e\u200e\
        # u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200f\u200f\
        # u200f\u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200f\u200e\
        # u200e\u200e\u200e\u200e\u200e\u200e\u200f\u200e\u200e\u200e\u200e\
        # u200f\u200e\u200e\u200e\u200f\u200f\u200f\u200f\u200f\u200e\u200e\
        # u200f\u200f\u200e\u200f\u200f\u200e\u200e\u200e\u200eON\u200e\u200f
        # \u200e\u200e\u200f\u200e",
        # may occur at random. Therefore, the "in" option is included.
        # TODO: determine why these artifacts may occur and/or remove them.
        if sub_val != main[sub_key] and sub_val not in main[sub_key]:
            return False
    return True
