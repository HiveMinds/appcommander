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
        for nodename in list(range(0, 1 + 1)):
            self.G.add_node(nodename)

        # Set root CA as trusted, on phone.

        # Set permissions of DAVx5 app.

        # Launch DAVx5 with adb command to pre-load configuration
        self.G.add_edge(0, 1, actions=[0])
        # CLick ok.

        self.G.add_edge(1, 2, actions=[0])
