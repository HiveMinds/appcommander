"""Verifies the given CLI arguments are valid in combination with each
other."""

from typeguard import typechecked


@typechecked
def assert_phone_is_connected() -> None:
    """Throws error if phone is not connected via ADB."""
    print("TODO: assert phone is connected to adb.")


@typechecked
def assert_app_is_installed(app_name: str) -> None:
    """Throws error if the app is installed on the phone."""
    assert_phone_is_connected()

    print(f"TODO: assert app is installed:{app_name}")


@typechecked
def assert_app_version_is_correct(app_version: str) -> None:
    """Throws error if the app version found on phone is not as expected."""
    assert_app_is_installed(app_version)

    print(f"TODO: assert app version is correct:{app_version}")
