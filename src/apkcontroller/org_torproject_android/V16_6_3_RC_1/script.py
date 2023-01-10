"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""

import importlib
from typing import Callable, Dict, List, Optional, Union

import networkx as nx
from typeguard import typechecked
from uiautomator import AutomatorDevice

from src.apkcontroller.helper import export_screen_data_if_valid
from src.apkcontroller.Screen import Screen

screen_path: str = "src.apkcontroller.org_torproject_android.V16_6_3_RC_1."
moduleNames = []
screen_func_names = []
modules = []
for screen_index in range(0, 8):
    module_name = f"{screen_path}screen_{screen_index}"
    moduleNames.append(module_name)
    screen_func_names.append(f"screen_{screen_index}")
    my_module = importlib.import_module(module_name)
    modules.append(my_module)


class Apk_script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
        device: Optional[AutomatorDevice] = None,
        torifying_apps: Optional[Dict[str, str]] = None,
    ) -> None:

        # Store data used to generate output and find Screen object files.
        self.script_description: Dict = {
            "title": "conf_orbot",
            "app_name": "org.torproject.android",
            "app_display_name": "Orbot",
            "version": "16.6.3 RC 1",
            "overwrite": True,
        }
        if torifying_apps is not None:
            self.script_description["torifying_apps"] = torifying_apps

        # Generate the script screen flow as a graph and generate the screens.
        self.script_graph = nx.DiGraph()
        self.screens: List[Screen] = self.create_screens(self.script_graph)

        # Export the data of the screens if they happen to be found in the
        # device already.
        if device is not None:
            export_screen_data_if_valid(
                device=device,
                overwrite=self.script_description["overwrite"],
                screens=self.screens,
            )

        # Specify the start and end nodes in the graph.
        self.specify_start__and_end_nodes(self.script_graph)

    @typechecked
    def create_screens(self, script_graph: nx.DiGraph) -> List[Screen]:
        """Creates the screens as networkx nodes.

        TODO: refactor to outside of script to reduce duplicate code.
        """
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
            screens.append(screen_function(self.script_description))

        # Add the screen objects to the script graph.
        for screen in screens:
            # TODO: verify all screen nrs are unique.
            script_graph.add_node(screen.script_description["screen_nr"])
            script_graph.nodes[screen.script_description["screen_nr"]][
                "Screen"
            ] = screen
        return screens

    @typechecked
    def specify_start__and_end_nodes(self, script_graph: nx.DiGraph) -> None:
        """Sets the is_start attributes to True in the nodes that are start
        screens.

        Sets the is_end attributes to True in the nodes that are end
        screens.
        """

        for nodename in script_graph.nodes:
            screen: Screen = script_graph.nodes[nodename]["Screen"]
            if screen.script_description["screen_nr"] in list(range(0, 8)):
                script_graph.nodes[nodename]["is_start"] = True
            else:
                script_graph.nodes[nodename]["is_start"] = False
            if screen.script_description["screen_nr"] in [7]:
                script_graph.nodes[nodename]["is_end"] = True
            else:
                script_graph.nodes[nodename]["is_end"] = False

    @typechecked
    def create_screen_transitions(self, script_graph: nx.DiGraph) -> None:
        """Adds the edges between the nodes(screens), representing possible
        transitions between the screens. The edges contain a list containing
        lists of actions.

        For example, it may be that actions: [click: checkmark I, click:
        Next], lead to screen 3, as well as actions: [click: Next] lead
        to screen 3. Hence, 1 edge multiple action lists (in/as a list).
        """
        print(f"TODO: set edges properties.{script_graph}")

    @typechecked
    def perform_action(
        self,
        device: AutomatorDevice,
        next_actions: List[Callable],
        screen_nr: int,
        additional_info: Dict[str, Union[str, bool]],
    ) -> None:
        """Performs the first action list in the list of action lists."""
        if screen_nr == 6:
            next_actions[0](
                device=device,
                additional_info=additional_info["torrifying_apps"],
            )
        else:
            next_actions[0](
                device=device,
                additional_info=additional_info["torrifying_apps"],
            )
