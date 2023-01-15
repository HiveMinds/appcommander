"""Stores the flow logic of the script in a networkx graph."""

from typeguard import typechecked

from src.appcommander.run_bash_code import run_bash_command


class App_input_data:
    """Stores the input data that is fed into the DAVx5 app."""

    # pylint: disable=R0903
    @typechecked
    def __init__(
        self,
        nextcloud_password: str,
        nextcloud_username: str,
        onion_url: str,
    ) -> None:
        """Creates the networkx graph with the screen nrs as nodes, and the
        action lists as edges."""
        self.nextcloud_password: str = nextcloud_password
        self.nextcloud_username: str = nextcloud_username
        self.onion_url: str = onion_url

    @typechecked
    def launch_app(
        self,
        package_name: str,
    ) -> None:
        """Launches DAVx5 with onion url of your Nextcloud server and your
        Nextcloud credentials."""

        print(f"Launching: {package_name}")
        # TODO: verify Nextcloud server is running on onion url.
        command = (
            "adb shell am start -a android.intent.action.VIEW -d caldavs://"
            + f"{self.nextcloud_username}:{self.nextcloud_password}@"
            + f"{self.onion_url}/remote.php"
            + f"/dav/principals/users/{self.nextcloud_username}"
        )

        print(f"command={command}")
        run_bash_command(
            await_compilation=True, bash_command=command, verbose=False
        )
