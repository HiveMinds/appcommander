"""Starts a script to control an app."""


from typeguard import typechecked


class Apk_script:
    """Experiment manager.

    First prepares the environment for running the experiment, and then
    calls a private method that executes the experiment consisting of 4
    stages.
    """

    # pylint: disable=R0903

    @typechecked
    def __init__(
        self,
    ) -> None:

        self.name = "org.torproject.android"
        self.display_name = "Orbot"
        self.version = "16.6.3 RC 1"

    @typechecked
    def run_script(self) -> None:
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
        print(self)
