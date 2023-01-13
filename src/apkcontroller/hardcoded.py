"""Contains hardcoded data."""

# keys: The app name as the user sees it.
# values: The app name on the Android filesystem.
from typing import Dict

app_name_mappings: Dict = {
    "Nextcloud": "org.nextcloud.android",
    "DAVx5": "at.bitfire.davdroid",
    "Orbot": "org.torproject.android",
}
# TODO: verify all supported package names are unique.
