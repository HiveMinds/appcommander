"""Completes the tasks specified in the arg_parser."""

import argparse

from typeguard import typechecked


@typechecked
def process_args(args: argparse.Namespace) -> None:
    """Processes the arguments and ensures the accompanying tasks are executed.

    TODO: --graph-filepath
    TODO: --run-config
    TODO: list existing exp_configs
    TODO: list existing exp_configs
    """
    print(args)
