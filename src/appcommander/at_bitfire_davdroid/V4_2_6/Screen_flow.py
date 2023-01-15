"""Stores the flow logic of the script in a networkx graph."""

import networkx as nx
from typeguard import typechecked


class Screen_flow:
    """Contains a map from screen number and action number to next expected
    screens."""

    # pylint: disable=R0903
    @typechecked
    def __init__(
        self,
    ) -> None:
        """Creates the networkx graph with the screen nrs as nodes, and the
        action lists as edges."""
        self.G = nx.DiGraph()
        for nodename in list(range(0, 5 + 1)):
            self.G.add_node(nodename)

        # Set root CA as trusted, on phone.

        # Set permissions of DAVx5 app.

        # Launch DAVx5 with adb command to pre-load configuration

        # Screen 0: CLick LOGIN.
        self.G.add_edge(0, 1, actions=[0])

        # Screen 1: If root CA is not trusted, install then restart flow.
        self.G.add_edge(1, 0, actions=[0])
        # Or click: "trust cert" in app and get additional prompt in screen 2.
        self.G.add_edge(1, 2, actions=[0])

        # Screen 2: Give name for certificate and press ok.
        self.G.add_edge(2, 4, actions=[0])

        # If OK was pressed before cert was set, set again with warning message
        # in screen 3, and press ok.
        self.G.add_edge(2, 3, actions=[0])
        self.G.add_edge(2, 5, actions=[0])

        # Screen 3: If OK was pressed before cert was set, set again with
        # warning message, and press ok.
        self.G.add_edge(3, 4, actions=[0])
        self.G.add_edge(3, 5, actions=[0])

        # Screen 4: Querying server.
        self.G.add_edge(4, 4, actions=[0])

        # Screen 5: set the name of the Nextcloud account in DAVx5.
        self.G.add_edge(4, 5, actions=[0])
