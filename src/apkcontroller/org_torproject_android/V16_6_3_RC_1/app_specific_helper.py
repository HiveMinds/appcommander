"""Functions to assist a script file for an arbitrary app."""
from typing import TYPE_CHECKING, Dict, List, Union, cast

from typeguard import typechecked

from src.appcommander.helper import dict_contains_other_dict

# pylint: disable=R0801
if TYPE_CHECKING:
    from src.appcommander.org_torproject_android.V16_6_3_RC_1.Script import (
        Script,
    )
    from src.appcommander.Screen import Screen
else:
    Screen = object
    Script = object


@typechecked
def get_torified_item_index_dict(
    required_object: Dict[str, str],
    unpacked_screen_dict: Dict[str, Union[List, Dict, str]],
    parent_dict: Union[List, Dict[str, Union[List, Dict, str]]],
) -> Dict:  # -> Dict[str, str]:
    """Parses the screen dictionary and returns the index of the item of the
    app that you want to torify. The item is found by checking if it has a
    "node" key, which has a List of 3 elements as value (each in the form of a
    dict):
     - the app icon.
     - the app name
     - the checkbox to torify that app.
    The dict with the app name is used to identify the relevant item, then the
    dictionary of that item contains the @index value, which is the index of
    that app in the Orbot configuration/torify apps screen. This method returns
    the complete item dictionary including the 3 node children.

    It recursively looks through the screen dict until it has found the app."""

    if dict_contains_other_dict(required_object, unpacked_screen_dict):
        return cast(Dict, parent_dict)
    if "node" in unpacked_screen_dict.keys():
        if isinstance(unpacked_screen_dict["node"], Dict):
            if get_torified_item_index_dict(
                required_object=required_object,
                unpacked_screen_dict=unpacked_screen_dict["node"],
                parent_dict=unpacked_screen_dict,
            ):
                return get_torified_item_index_dict(
                    required_object=required_object,
                    unpacked_screen_dict=unpacked_screen_dict["node"],
                    parent_dict=unpacked_screen_dict,
                )
        if isinstance(unpacked_screen_dict["node"], List):

            # A item in the Orbot app consists of an icon, app_name and
            # checkbox. So if the length of this node List is three, and it
            # contains the app name in the dict of the first index of the list
            # elements, one wants the index of the actual dict that has this
            # node list, because that dict has the index of the item.
            if len(unpacked_screen_dict["node"]) == 3:
                if dict_contains_other_dict(
                    required_object, unpacked_screen_dict["node"][1]
                ):
                    return unpacked_screen_dict

            # Keep on searching deeper otherwise.
            for node_elem in unpacked_screen_dict["node"]:
                if get_torified_item_index_dict(
                    required_object=required_object,
                    unpacked_screen_dict=cast(Dict, node_elem),
                    parent_dict=unpacked_screen_dict["node"],
                ):
                    return get_torified_item_index_dict(
                        required_object=required_object,
                        unpacked_screen_dict=cast(Dict, node_elem),
                        parent_dict=unpacked_screen_dict["node"],
                    )
        if not isinstance(unpacked_screen_dict["node"], Dict | List):
            raise TypeError("Node value of unexpected type.")
    return {}


def orbot_torifying_app_is_checked(app_item: Dict) -> bool:
    """Returns True if the item is checked, False if it is unchecked."""
    if "@checkable" not in app_item["node"][2].keys():
        raise KeyError(
            "Error, the app checkbox should contain @checkable."
            + f"Though it did not:{app_item}"
        )
    if "@checkable" not in app_item["node"][2]["@checkable"] != "true":
        raise ValueError(
            "Error, the app checkbox should contain:"
            + f"@checkable: true Though it did not:{app_item}"
        )
    if app_item["node"][2]["@checked"] == "true":
        return True
    if app_item["node"][2]["@checked"] == "false":
        return False
    raise KeyError(
        "Error, valid @checked value was not found in app_item checkbox."
    )
