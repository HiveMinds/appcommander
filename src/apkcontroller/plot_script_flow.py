"""Plots the script flow."""
from typing import Dict, List, Union

import matplotlib.pyplot as plt
import networkx as nx
import PIL
from typeguard import typechecked


def visualise_script_flow(
    G: nx.DiGraph, app_name: str, app_version: str
) -> None:
    """Visualises the script flow."""

    G.nodes[0]["pos"] = [0, 0]
    set_cyclical_node_coords(evaluated_nodes=[], G=G, start_nodename=0, y=0)
    set_node_images(G=G, app_name=app_name, app_version=app_version)
    plot_coordinated_graph(
        G=G,
    )


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


def set_node_images(G: nx.DiGraph, app_name: str, app_version: str) -> None:
    """Sets the phone screens as node images to visualise the script flow
    between screens."""
    # Image URLs for graph nodes
    icons: Dict[str, str] = {}
    for screen_nr in G.nodes:
        icons[screen_nr] = (
            f"src/appcommander/{app_name}/V{app_version}/verified/"
            + f"{screen_nr}.png"
        )
        # TODO: verify file exists, use dummy file otherwise.
    # Load images
    images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

    # Generate the computer network graph
    for nodename in G.nodes:
        G.nodes[nodename]["image"] = images[nodename]


@typechecked
def plot_coordinated_graph(
    G: Union[nx.Graph, nx.DiGraph],
) -> None:
    """Plots the networkx graph with images instead of nodes.

    :param G: The original graph on which the MDSA algorithm is ran.
    """
    pos: Dict[int, List[int]] = {}
    for nodename in G.nodes:
        pos[nodename] = G.nodes[nodename]["pos"]
    print(f"pos={pos}")

    fig = plt.figure(figsize=(1, 1))
    ax = plt.subplot(111)
    ax.set_aspect("equal")
    nx.draw_networkx_edges(G, pos, ax=ax)

    # plt.xlim(-1,10)
    # plt.ylim(-1.5,1.5)

    trans = ax.transData.transform
    trans2 = fig.transFigure.inverted().transform

    piesize = 0.3  # this is the image size
    p2 = piesize / 2.0
    for n in G:
        xx, yy = trans(pos[n])  # figure coordinates
        xa, ya = trans2((xx, yy))  # axes coordinates
        print(f"n={n},xa,ya={xa,ya}")
        a = plt.axes([xa - p2, ya - p2, piesize, piesize])
        a.set_aspect("equal")
        a.imshow(G.nodes[n]["image"])
        a.axis("off")

    ax.axis("off")
    plt.show()
