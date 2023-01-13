"""Stores the flow logic of the script in a networkx graph."""

import networkx as nx
from typeguard import typechecked


class Script_flow:
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
        for nodename in list(range(0, 7 + 1)):
            self.G.add_node(nodename)
        self.G.add_edge(0, 1, actions=[0])

        self.G.add_edge(1, 2, actions=[0])
        self.G.add_edge(2, 3, actions=[0])
        self.G.add_edge(3, 4, actions=[0])
        self.G.add_edge(4, 5, actions=[0])
        self.G.add_edge(4, 7, actions=[0])

        self.G.add_edge(5, 6, actions=[0])
        # self.G.add_edge(5, 5, actions=[1])
        self.G.add_edge(5, 7, actions=[1])

        self.G.add_edge(6, 5, actions=[0])
        self.G.add_edge(6, 7, actions=[0])

        self.G.add_edge(7, 6, actions=[0])
