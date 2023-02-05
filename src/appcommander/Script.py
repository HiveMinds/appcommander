"""Script to run through Orbot app configuration.

Android names this app: org.torproject.android
"""


from typing import TYPE_CHECKING, Any, Dict, List, Union

from typeguard import typechecked

from appcommander.create_screens import create_screens, load_script_attribute

if TYPE_CHECKING:
    from appcommander.Screen import Screen
else:
    Screen = object


# pylint: disable=R0902
class Script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903
    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        app_name: str,
        overwrite: bool,
        package_name: str,
        version: str,
        cli_input_data: Dict[str, Union[str, Dict[str, str]]],
    ) -> None:
        self.app_name: str = app_name
        self.overwrite: bool = overwrite
        self.package_name: str = package_name
        self.package_name_dir: str = self.package_name.replace(
            ".", "_"
        ).replace(" ", "_")
        # self.torifying_apps: Union[Dict[str, str], None] = torifying_apps
        self.version: str = version
        self.version_dir: str = self.version.replace(".", "_").replace(
            " ", "_"
        )

        self.app_version_mod_path: str = (
            f"appcommander.{self.package_name_dir}.V{self.version_dir}."
        )
        self.app_version_dir: str = (
            f"src/appcommander/{self.package_name_dir}/V{self.version_dir}/"
        )

        # Create placeholder for past screens.
        self.past_screens: List[int] = []

        # Generate the script screen flow as a graph and generate the screens.
        # self.script_graph = load_graph(self.app_version_mod_path)
        self.script_graph = load_script_attribute(
            app_version_mod_path=self.app_version_mod_path,
            filename="Screen_flow",
            obj_name="Screen_flow",
            attribute_name="G",
        )
        self.input_data = load_script_attribute(
            app_version_mod_path=self.app_version_mod_path,
            filename="App_input_data",
            obj_name="App_input_data",
        )
        self.input_data = fill_input_data(
            self.input_data,
            cli_input_data,
        )
        self.screens: List[Screen] = create_screens(self)


@typechecked
def fill_input_data(  # type:ignore[misc]
    input_data: Any,
    cli_input_data: Dict,
) -> Any:
    """Stores the CLI input data into the input_data object, with appropriate
    typing."""
    # The ** unpacks the dictionary into the object.
    # TODO: test what happens if the dictionary is under- or overcomplete.
    return input_data(**cli_input_data)
