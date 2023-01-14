"""Functions to assist a script file for an arbitrary app."""
import importlib
from types import ModuleType
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

import networkx as nx
from typeguard import typechecked

if TYPE_CHECKING:
    from src.appcommander.Screen import Screen
    from src.appcommander.Script import Script
else:
    Script = object
    Screen = object


@typechecked
def create_screens(script: Script) -> List[Screen]:
    """Creates the screens as networkx nodes."""

    modules, screen_func_names = load_screen_files_per_app_version(
        script.app_version_mod_path, script.script_graph
    )
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
        script.script_graph.nodes[screen.screen_nr]["Screen"] = screen
    return screens


@typechecked
def load_screen_files_per_app_version(
    app_version_mod_path: str, graph: nx.DiGraph
) -> Tuple[List[ModuleType], List[str]]:
    """A module is a python file (in this case).

    So this script loads the Python files from which the screen object
    data is loaded. Each app and version has its own screen_x files.
    """

    # Specify path to screen_files
    moduleNames = []
    screen_func_names = []
    modules = []
    for screen_index in range(0, len(graph)):
        module_name = f"{app_version_mod_path}screen_{screen_index}"
        moduleNames.append(module_name)
        screen_func_names.append(f"screen_{screen_index}")
        my_module = importlib.import_module(module_name)
        modules.append(my_module)
    return modules, screen_func_names


@typechecked
def load_script_attribute(  # type:ignore[misc]
    app_version_mod_path: str,
    filename: str,
    obj_name: str,
    attribute_name: Optional[str] = None,
) -> Any:
    """Loads an attribute for the script object.

    If attribute_name is empty, it will load the object named <filename>
    inside the <filename>, otherwise it will load the attribute
    <attribute_name> of that object.
    """

    file_path = f"{app_version_mod_path}{filename}"
    imported_file = importlib.import_module(file_path)

    the_object = getattr(imported_file, obj_name)
    if attribute_name is not None:
        attribute = getattr(the_object(), attribute_name)
        return attribute
    return the_object
