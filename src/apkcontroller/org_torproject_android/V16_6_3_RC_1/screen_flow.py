"""Stores the flow logic of the script in a networkx graph."""


from typing import List

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

        self.G.add_edge(5, 6, actions=[0])
        self.G.add_edge(5, 5, actions=[1])
        self.G.add_edge(5, 7, actions=[1])

        self.G.add_edge(6, 5, actions=[0])
        self.G.add_edge(6, 7, actions=[0])

        self.G.add_edge(7, 6, actions=[0])


def get_expected_screen_nrs(
    G: nx.DiGraph, screen_nr: int, action_nr: int
) -> List[int]:
    """Returns the expected screens per screen per action."""
    expected_screens: List[int] = []
    for edge in G.edges:
        if edge[0] == screen_nr:
            print(f"screen_nr={screen_nr}")
            if action_nr in G[edge[0]][edge[1]]["actions"]:
                expected_screens.append(edge[1])
    return expected_screens
