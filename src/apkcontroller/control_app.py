"""Starts a script to control an app."""


from typeguard import typechecked


@typechecked
def run_script(script: str) -> None:
    """Runs the incoming script on the phone."""
    # Script folder structure:
    # app_scripts/app_name/version

    # Open the app.

    # Detect screen (wait for n seconds).

    # If invalid screen is detected/if valid screen is not found within n
    # seconds:
    # raise Exception.
    # Ideally include automatic issue creation (with optional screenshot.)
    # Else:

    # Perform optional additional verification.
    # Optional get and store some state.

    # Determine what next screen is.

    # Find dataform.
    # Fill dataform.
    # Optional: verify dataform is filled correctly.

    # Find button.
    # Click button.
    # Recursively go to next screen.
    print(script)
