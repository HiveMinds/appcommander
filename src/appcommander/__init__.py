"""Contains the project versioning."""
from appcommander.verification.arg_verification import verify_args

from .arg_parser.arg_parser import parse_cli_args
from .arg_parser.process_args import process_args

__version__ = "0.0.20"
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())


# Parse command line interface arguments to determine what this script does.
args = parse_cli_args()
verify_args(
    args,
)
process_args(
    args,
)
