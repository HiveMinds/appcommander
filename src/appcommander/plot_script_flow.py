"""Plots the script flow."""
import copy
import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import PIL
from matplotlib.pyplot import imread
from PIL import Image
from typeguard import typechecked


class Params:
    """Contains values to plot screen flow."""

    # pylint: disable=R0903
    # pylint: disable=R0913
    @typechecked
    def __init__(
        self,
        x_pos_multiplier: float,
        y_pos_multiplier: float,
        height: int,
        width: int,
        screen_size: float,
    ) -> None:
        """Contains values to plot screen flow."""
        self.x_pos_multiplier: float = x_pos_multiplier
        self.y_pos_multiplier: float = y_pos_multiplier
        self.height: int = height
        self.width: int = width
        self.screen_size: float = screen_size


def create_params() -> List[Params]:
    """Generates a brute-force range to loop over."""
    param_list = []
    # for x_pos_multiplier in np.arange(0,5,0.5): # 50
    for x_pos_multiplier in range(0, 1):  # 50
        for y_pos_multiplier in np.arange(0.5, 5, 0.5):  # 2500
            for height in range(6, 60, 5):  # 15.000
                for width in range(6, 60, 5):  # 15.000
                    for screen_size in np.arange(0.01, 2, 0.05):
                        param = Params(
                            x_pos_multiplier=x_pos_multiplier,
                            y_pos_multiplier=y_pos_multiplier,
                            height=height,
                            width=width,
                            screen_size=screen_size,
                        )
                        param_list.append(param)
    return param_list


def visualise_script_flow(
    G: nx.DiGraph, package_name: str, app_version: str
) -> None:
    """Visualises the script flow."""
    param_list = create_params()

    img_width, img_height = get_existing_image_size(
        G=G,
        package_name=package_name,
        app_version=app_version,
    )
    resize_image(
        "Unknown_screen.png", target_width=img_width, target_height=img_height
    )

    G.nodes[0]["pos"] = [0, 0]
    set_cyclical_node_coords(evaluated_nodes=[], G=G, start_nodename=0, y=0)

    retry_plot_coordinated_graph(
        app_version=app_version,
        G=G,
        package_name=package_name,
        param_list=param_list,
    )


# pylint: disable=R0914
@typechecked
def retry_plot_coordinated_graph(
    app_version: str,
    G: Union[nx.Graph, nx.DiGraph],
    package_name: str,
    param_list: List[Params],
) -> None:
    """Plots the networkx graph with images instead of nodes.

    :param G: The original graph on which the MDSA algorithm is ran.
    """
    for param in param_list:
        pos: Dict[int, List[int]] = {}
        for nodename in G.nodes:
            pos[nodename] = copy.deepcopy(G.nodes[nodename]["pos"])
            if pos[nodename][1] > 0:
                pos[nodename][1] = pos[nodename][1] - 1
            pos[nodename][1] = (  # type:ignore[call-overload]
                pos[nodename][1] * param.y_pos_multiplier
            )
            print(f"{nodename}: {pos[nodename]}")
        # TODO: normalise towards center,
        # TODO: remove skipped horizontal positions.

        # fig = plt.figure(figsize=(1, 1))
        # ax = plt.subplot(111)
        # ax.set_aspect("equal")

        for screen_nr in G.nodes:
            sample_img_path = (
                f"src/appcommander/{package_name}/V{app_version}/verified/"
                + f"{screen_nr}.png"
            )
            if Path(sample_img_path).is_file():
                img = imread(sample_img_path)
            else:
                img = imread("Unknown_screen.resized")

            G.add_node(screen_nr, image=img)

        fig = plt.figure(figsize=(param.width, param.height))
        ax = plt.subplot(111)

        horizontal_edges, vertical_edges = get_horizontal_and_vertical_edges(
            G=G
        )
        G.remove_edges_from(list(G.edges()))

        # draw vertical edges using a larger node size
        for edge in vertical_edges:
            if edge not in G.edges:
                G.add_edge(edge[0], edge[1])

        nx.draw_networkx_edges(G, pos, ax=ax, node_size=8000, arrowsize=30)

        # add the horizontal edges with a smaller node size
        for edge in horizontal_edges:
            if edge not in G.edges:
                G.add_edge(edge[0], edge[1])
        nx.draw_networkx_edges(G, pos, ax=ax, node_size=3000, arrowsize=30)

        set_node_images(
            G=G, package_name=package_name, app_version=app_version
        )

        trans = ax.transData.transform
        trans2 = fig.transFigure.inverted().transform

        piesize = param.screen_size  # this is the image size
        p2 = piesize / 2.0
        for n in G:
            xx, yy = trans(pos[n])  # figure coordinates
            xa, ya = trans2((xx, yy))  # axes coordinates
            a = plt.axes([xa - p2, ya - p2, piesize, piesize])
            a.set_aspect("equal")
            a.imshow(G.nodes[n]["image"])
            a.axis("off")
        ax.axis("off")
        # plt.savefig(f"src/appcommander/{package_name}/V{app_version}/flow.png")
        print(param.__dict__)
        plt.savefig(f"images/{param.__dict__}.png")


def set_cyclical_node_coords(
    evaluated_nodes: List[int],
    G: nx.DiGraph,
    start_nodename: int,
    y: int,
) -> nx.DiGraph:
    """Sets the coordinates for a cyclical graph."""
    neighbors = list(G.neighbors(start_nodename))
    if "pos" not in G.nodes[start_nodename].keys():
        raise KeyError("Error, pos value of start node was not set.")
    for x, neighbor in enumerate(neighbors):
        if neighbor not in evaluated_nodes:
            if "pos" not in G.nodes[neighbor].keys():
                G.nodes[neighbor]["pos"] = [y + 1, x]
    for x, neighbor in enumerate(neighbors):
        if neighbor not in evaluated_nodes:
            evaluated_nodes.append(neighbor)
            set_cyclical_node_coords(
                evaluated_nodes=evaluated_nodes,
                G=G,
                start_nodename=neighbor,
                y=y + 1,
            )


def set_node_images(
    G: nx.DiGraph, package_name: str, app_version: str
) -> None:
    """Sets the phone screens as node images to visualise the script flow
    between screens."""
    # Image URLs for graph nodes
    icons: Dict[str, str] = {}
    for screen_nr in G.nodes:
        img_path = (
            f"src/appcommander/{package_name}/V{app_version}/verified/"
            + f"{screen_nr}.png"
        )
        if Path(img_path).is_file():
            icons[screen_nr] = img_path
        else:
            icons[screen_nr] = "Unknown_screen.png"

        # TODO: verify file exists, use dummy file otherwise.
    # Load images
    images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

    # Generate the computer network graph
    for nodename in G.nodes:
        G.nodes[nodename]["image"] = images[nodename]


def get_horizontal_and_vertical_edges(
    G: nx.DiGraph,
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """Returns the vertical edges, and the horizontal edges."""
    horizontal: List[Tuple[int, int]] = []
    vertical: List[Tuple[int, int]] = []

    for edge in G.edges:
        left = edge[0]
        right = edge[1]
        if G.nodes[left]["pos"][1] != G.nodes[right]["pos"][1]:
            vertical.append(edge)
        else:
            horizontal.append(edge)
    return horizontal, vertical


def resize_image(
    input_filepath: str,
    target_height: int,
    target_width: int,
) -> None:
    """Stretch an image into a specific resolution."""

    if Path(input_filepath).is_file():
        outfile = os.path.splitext(input_filepath)[0] + ".resized"
        if input_filepath != outfile:
            try:
                img = Image.open(input_filepath)
                # im.thumbnail(size, Image.Resampling.LANCZOS)
                img = img.resize(
                    (target_width, target_height), Image.ANTIALIAS
                )
                img.save(outfile, "png")
            except OSError:
                print(f"Cannot resise image:{input_filepath}")
    else:
        raise FileNotFoundError(f"Error:{input_filepath}")


def get_existing_image_size(
    G: Union[nx.Graph, nx.DiGraph],
    package_name: str,
    app_version: str,
) -> Tuple[int, int]:
    """Loop through the existing screen png files, and returns the dimensions
    of the first screen png."""
    for screen_nr in G.nodes:
        img_path = (
            f"src/appcommander/{package_name}/V{app_version}/verified/"
            + f"{screen_nr}.png"
        )
        if Path(img_path).is_file():
            im = Image.open(img_path)
            width, height = im.size
            return width, height
    raise FileNotFoundError("Error, no screen found.")
