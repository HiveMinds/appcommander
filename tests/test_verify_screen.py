"""Verifies 2 nodes are included in the networkx graph."""
import unittest
from typing import Dict, List

from typeguard import typechecked

from appcommander.helper import (
    load_json_file_into_dict,
    required_objects_in_screen,
)


class Test_get_graph(unittest.TestCase):
    """Tests whether the get_networkx_graph_of_2_neurons of the get_graph file
    returns a graph with 2 nodes."""

    # Initialize test object
    @typechecked
    def __init__(self, *args, **kwargs) -> None:  # type:ignore[no-untyped-def]
        super().__init__(*args, **kwargs)

    @typechecked
    def test_finds_required_dict(self) -> None:
        """Tests whether the required_object_in_screen function correctly finds
        the required object in s0."""
        screen_dict: Dict = load_json_file_into_dict(
            "src/appcommander/org.torproject.android/" + "16.6.3 RC 1/s0.json"
        )

        required_objects: List[Dict[str, str]] = [
            {
                "@package": "org.torproject.android",
                "@text": "Global (Auto)",
            },
        ]
        self.assertTrue(
            required_objects_in_screen(
                required_objects, screen_dict["hierarchy"]
            )
        )
        required_objects = [
            {
                "@resource-id": "android:id/text1",
            },
        ]
        self.assertTrue(
            required_objects_in_screen(
                required_objects, screen_dict["hierarchy"]
            )
        )

        #
        # "@text": "Trouble " "connecting?",
        # "@text": "Use Bridges",
        # "@text": "Orbot",
