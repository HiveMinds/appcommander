"""Verifies 2 nodes are included in the networkx graph."""
import unittest
from typing import Any, Dict, List

from typeguard import typechecked

from src.apkcontroller.helper import element_in_ui
from src.apkcontroller.scripts.s2 import s2


class Test_get_graph(unittest.TestCase):
    """Tests whether the get_networkx_graph_of_2_neurons of the get_graph file
    returns a graph with 2 nodes."""

    # Initialize test object
    @typechecked
    def __init__(self, *args, **kwargs) -> None:  # type:ignore[no-untyped-def]
        super().__init__(*args, **kwargs)

    @typechecked
    def test_finds_required_dict(self) -> None:
        """Tests whether the element_in_ui function correctly finds the
        required object in s0."""

        required_objects: List[Dict[str, Any]] = {
            "@package": "org.torproject.android",
            "@text": "Global (Auto)",
        }
        self.assertTrue(element_in_ui(required_objects, s2["hierarchy"]))
        required_objects: List[Dict[str, Any]] = {
            "@resource-id": "android:id/text1",
        }
        self.assertTrue(element_in_ui(required_objects, s2["hierarchy"]))

        #
        # "@text": "Trouble " "connecting?",
        # "@text": "Use Bridges ",
        # "@text": "Orbot",
