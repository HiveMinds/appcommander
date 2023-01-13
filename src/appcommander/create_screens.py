"""Functions to assist a script file for an arbitrary app."""
import importlib
from typing import TYPE_CHECKING, List

import networkx as nx
from typeguard import typechecked

if TYPE_CHECKING:
    from src.appcommander.org_torproject_android.V16_6_3_RC_1.Script import (
        Script,
    )
    from src.appcommander.Screen import Screen
else:
    Script = object
    Screen = object

screen_path: str = "src.appcommander.org_torproject_android.V16_6_3_RC_1."
moduleNames = []
screen_func_names = []
modules = []
for screen_index in range(0, 8):
    module_name = f"{screen_path}screen_{screen_index}"
    moduleNames.append(module_name)
    screen_func_names.append(f"screen_{screen_index}")
    my_module = importlib.import_module(module_name)
    modules.append(my_module)


@typechecked
def create_screens(script_graph: nx.DiGraph) -> List[Screen]:
    """Creates the screens as networkx nodes."""
    screens: List[Screen] = []

    # Create the Screen objects programmatically.
    for i, module in enumerate(modules):
        # Create the function (reference) programmatically.
        # module represents the file that contains the screen function.
        # screen_func_name[i] is the name of the screen_i function in that
        # module.
        # screen_function is the actual Pythonic function handle. it is
        # like writing: screen_3 if i==3.
        screen_function = getattr(module, screen_func_names[i])
        # execute the screen function, which returns a Screen object.
        screens.append(screen_function())

    # Add the screen objects to the script graph.
    for screen in screens:
        script_graph.nodes[screen.screen_nr]["Screen"] = screen
    return screens
