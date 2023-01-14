"""Stores the flow logic of the script in a networkx graph."""

from typeguard import typechecked


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
