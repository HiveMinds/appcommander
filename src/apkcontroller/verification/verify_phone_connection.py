"""Verifies the given CLI arguments are valid in combination with each
other."""

from typeguard import typechecked


@typechecked
def assert_phone_is_connected() -> None:
    """Throws error if phone is not connected via ADB."""
    print("TODO: assert phone is connected to adb.")


@typechecked
def assert_app_is_installed() -> None:
    """Throws error if the app is installed on the phone."""
    assert_phone_is_connected()

    print("TODO: assert app is installed.")


@typechecked
def assert_app_version_is_correct(app_version: str) -> None:
    """Throws error if the app version is not as expected."""
    assert_app_is_installed()

    print("TODO: assert app version is correct.")
    print(app_version)
