"""Performs verifications on the status of the phone."""
from typing import TYPE_CHECKING, Dict, List, Tuple

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from appcommander.helper import (
    export_screen_data,
    get_screen_as_dict,
    is_expected_screen,
)
from appcommander.script_orientation import get_expected_screens

# pylint: disable=R0801
if TYPE_CHECKING:
    from appcommander.Screen import Screen
    from appcommander.Script import Script
else:
    Screen = object
    Script = object


@typechecked
def can_proceed(
    dev: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script: Script,
) -> Tuple[bool, int]:
    """Checks whether the screen is expected, raises an error if not.

    And it returns the current screen number.
    """
    # get current screen dict.
    unpacked_screen_dict: Dict = get_screen_as_dict(
        dev=dev,
        unpack=True,
        screen_dict={},
        reload=False,
    )

    # verify current_screen in next_screens.
    is_expected, screen_nr = current_screen_is_expected(
        dev=dev,
        expected_screennames=expected_screennames,
        retry=retry,
        script_graph=script.script_graph,
        unpacked_screen_dict=unpacked_screen_dict,
    )

    # end_screens = get end_screens()
    if not is_expected:
        # Export the actual screen, screen data and expected screens in
        # specific error log folder.
        export_screen_data(
            dev=dev,
            screen_dict=unpacked_screen_dict,
            screen_nr=screen_nr,
            script=script,
            overwrite=True,
            subdir="error",
        )
        raise ReferenceError(
            f"Error, the expected screen was not found in:{screen_nr}. "
            + f"Searched for:{expected_screennames}. The accompanying screen "
            + "and xml can be found in:src/appcommander/<package_name>/<app_"
            + f"version>/error/{screen_nr}.json"
        )
    return is_expected, screen_nr


@typechecked
def current_screen_is_expected(
    dev: AutomatorDevice,
    expected_screennames: List[int],
    retry: bool,
    script_graph: nx.DiGraph,
    unpacked_screen_dict: Dict,
) -> Tuple[bool, int]:
    """Determines whether the current screen is one of the expected screens."""
    expected_screens: List[Screen] = get_expected_screens(
        expected_screennames, script_graph
    )
    for expected_screen in expected_screens:
        if is_expected_screen(
            dev=dev,
            expected_screen=expected_screen,
            retry=retry,
            unpacked_screen_dict=unpacked_screen_dict,
        ):

            return (
                True,
                int(str(expected_screen.screen_nr)),
            )
    return (False, -1)
