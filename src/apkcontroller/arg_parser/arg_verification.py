"""Verifies the given CLI arguments are valid in combination with each
other."""
import argparse
import json

from typeguard import typechecked

from ..helper import file_exists


@typechecked
def verify_args(args: argparse.Namespace) -> None:
    """Performs the checks to verify the parser."""
    if isinstance(args.script, str):
        verify_input_graph_path(args.script)


@typechecked
def verify_input_graph_path(graph_path: str) -> None:
    """Verifies the filepath for the input graph exists and contains a valid
    networkx graph."""
    # Assert graph file exists.
    if not file_exists(graph_path):
        raise FileNotFoundError(f"Input Graph path was invalid:{graph_path}")

    # Read output JSON file into dict.
    with open(graph_path, encoding="utf-8") as json_file:
        json_graph = json.load(json_file)
        json_file.close()
    print(json_graph)
