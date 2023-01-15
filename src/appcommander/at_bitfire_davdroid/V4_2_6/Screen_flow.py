"""Stores the flow logic of the script in a networkx graph."""

import networkx as nx
from typeguard import typechecked


# pylint: disable=R0903
class Screen_flow:
    """Contains a map from screen number and action number to next expected
    screens."""

    # pylint: disable=R0904
    @typechecked
    def __init__(
        self,
    ) -> None:
        """Creates the networkx graph with the screen nrs as nodes, and the
        action lists as edges."""
        self.G = nx.DiGraph()
        for nodename in list(range(0, 8 + 1)):
            self.G.add_node(nodename)

        # Set root CA as trusted, on phone.

        # Set permissions of DAVx5 app.

        # Launch DAVx5 with adb command to pre-load configuration

        # Screen 0: CLick LOGIN.
        self.G.add_edge(0, 1, actions=[0])

        # Screen 1: querying the Nextcloud server over tor.
        self.G.add_edge(1, 1, actions=[0])  # Not found.
        self.G.add_edge(1, 2, actions=[0])  # Not found.
        self.G.add_edge(1, 3, actions=[0])  # Found. cert not yet trusted.
        self.G.add_edge(1, 4, actions=[0])  # Found, cert trusted.
        self.G.add_edge(1, 6, actions=[0])  # Done, enter DAVx5 accountname.

        # TODO: Was not able to connect to tor. Restart orbot and try again.
        self.G.add_edge(2, 0, actions=[0])

        # Screen 3: If root CA is not trusted, install then restart flow.
        self.G.add_edge(3, 0, actions=[0])
        self.G.add_edge(3, 1, actions=[0])
        # Or click: "trust cert" in app and get additional prompt in screen 3.
        self.G.add_edge(3, 4, actions=[0])
        self.G.add_edge(3, 5, actions=[0])
        self.G.add_edge(3, 6, actions=[0])

        # Screen 4: Give name for certificate and press ok.
        self.G.add_edge(4, 6, actions=[0])

        # If OK was pressed before cert was set, set again with warning message
        # in screen 4, and press ok.
        self.G.add_edge(4, 5, actions=[0])

        # Screen 5: If OK was pressed before cert was set, set again with
        # warning message, and press ok.
        self.G.add_edge(5, 6, actions=[0])

        # Screen 6: set the name of the Nextcloud account in DAVx5.
        self.G.add_edge(6, 7, actions=[0])

        self.G.add_edge(7, 8, actions=[0])
