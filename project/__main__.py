import os

from project.graph_utils import (
    get_info,
    create_labeled_two_cycles_graph,
    save_graph_to_file,
)

if __name__ == "__main__":
    g = create_labeled_two_cycles_graph(3, 5, edge_labels=("c", "d"))
    save_graph_to_file(g, os.sep.join(["..", "output", "graph"]))
    print(get_info(g))
