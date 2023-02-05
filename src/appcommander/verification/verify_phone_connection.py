"""Verifies the given CLI arguments are valid in combination with each
other."""

from typing import List

from typeguard import typechecked

from appcommander.helper import run_bash_command


@typechecked
def assert_phone_is_connected() -> None:
    """Throws error if phone is not connected via ADB."""
    # Launc the app on phone.
    command = "adb devices"
    output = run_bash_command(
        await_compilation=True, bash_command=command, verbose=False
    )
    lines = output.split("\n")

    found_device: bool = False
    # TODO: make more robust check, e.g. eat "List of devs attached" and see
    # whether any a-Z 0-9 characters exist in output.
    for line in lines:
        if "List of devices attached" not in line:
            for letter in line:
                if letter.isalnum():
                    found_device = True

    if not found_device:
        raise Exception("Error, no adb dev is found.")

    # TODO: check if more than one devs are connected, and if yes, raise
    # exception if user did not specify the desired dev name.


@typechecked
def assert_app_is_installed(package_name: str) -> None:
    """Throws error if the app is installed on the phone."""
    assert_phone_is_connected()
    command = "adb shell pm list packages"
    output = run_bash_command(
        await_compilation=True, bash_command=command, verbose=False
    )
    installed_package_list: List[str] = list(set(output.split("\n")))
    installed_packages = list(
        map(
            lambda x: x.replace("package:", "").replace("'", ""),
            installed_package_list,
        )
    )

    if package_name not in installed_packages:
        raise Exception(
            f"Error, the app:'{package_name}' with package name:'"
            + f"{package_name}', is not yet installed:"
            + f"{sorted(installed_packages)}"
        )


@typechecked
def assert_app_version_is_correct(package_name: str, app_version: str) -> None:
    """Throws error if the app version found on phone is not as expected."""
    assert_app_is_installed(package_name=package_name)

    print(f"TODO: assert app version is correct:{app_version}")
