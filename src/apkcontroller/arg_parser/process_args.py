"""Completes the tasks specified in the arg_parser."""

import argparse

from typeguard import typechecked

from src.apkcontroller.verification.verify_phone_connection import (
    assert_app_is_installed,
    assert_app_version_is_correct,
)


@typechecked
def process_args(args: argparse.Namespace) -> None:
    """Processes the arguments and ensures the accompanying tasks are
    executed."""
    print(args)

    # Also verifies phone is connected.
    # if version is passed:
    assert_app_is_installed()
    # else:
    assert_app_version_is_correct("TODO: version")
