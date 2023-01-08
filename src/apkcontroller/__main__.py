"""Entry point for this project, runs the project code based on the cli command
that invokes this script."""


from src.apkcontroller.helper import show_screen_as_dict
from src.apkcontroller.scripts.org_torproject_android import Apk_script
from src.apkcontroller.verification.arg_verification import verify_args

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
apk_script = Apk_script()

from uiautomator import device as d

# d(resourceId="org.torproject.android:id/ivAppVpnSettings").click()
screen_dict = show_screen_as_dict(d)
# d(resourceId='org.torproject.android:id/btnStart').click()
# In circle:
# ...
# Below:
# Orbot is starting...
