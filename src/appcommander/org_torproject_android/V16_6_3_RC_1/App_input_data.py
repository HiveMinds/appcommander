"""Stores the flow logic of the script in a networkx graph."""

from typing import Dict

from typeguard import typechecked

from appcommander.run_bash_code import run_bash_command


class App_input_data:
    """Stores the input data that is fed into the DAVx5 app."""

    # pylint: disable=R0903
    @typechecked
    def __init__(
        self,
        torifying_apps: Dict[str, str],
    ) -> None:
        """Creates the networkx graph with the screen nrs as nodes, and the
        action lists as edges."""
        self.torifying_apps: Dict[str, str] = torifying_apps

    @typechecked
    def launch_app(
        self,
        package_name: str,
    ) -> None:
        """Launches the Orbot app."""
        print(f"Launching:{package_name}")

        # Launch the app on phone.
        command = f'adb shell monkey -p "{package_name}" 1 &>/dev/null'
        run_bash_command(
            await_compilation=True, bash_command=command, verbose=False
        )
