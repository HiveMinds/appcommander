"""Runs bash commands."""
import subprocess  # nosec
from typing import Union

from typeguard import typechecked


@typechecked
def run_bash_command(
    await_compilation: bool, bash_command: str, verbose: bool
) -> Union[None, str]:
    """Runs a bash command."""
    if await_compilation:
        if verbose:
            subprocess.call(bash_command, shell=True)  # nosec
        else:
            output = subprocess.check_output(  # nosec
                bash_command,
                shell=True,
                # stderr=subprocess.DEVNULL,
                # stdout=subprocess.DEVNULL,
            )
            return output.decode("utf-8")
    else:
        if verbose:
            # pylint: disable=R1732
            subprocess.Popen(bash_command, shell=True)  # nosec
        else:
            # pylint: disable=R1732
            subprocess.Popen(  # nosec
                bash_command,
                shell=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
    return None
