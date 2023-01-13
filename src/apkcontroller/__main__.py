"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""


from src.appcommander.verification.arg_verification import verify_args

from .arg_parser.arg_parser import parse_cli_args
from .arg_parser.process_args import process_args

# Parse command line interface arguments to determine what this script does.
args = parse_cli_args()
verify_args(
    args,
)
process_args(
    args,
)
