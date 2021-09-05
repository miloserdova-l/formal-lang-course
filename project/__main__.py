import os

from project.graph_utils import (
    get_info,
    create_labeled_two_cycles_graph,
    save_graph_to_file,
)

if __name__ == "__main__":
    g = create_labeled_two_cycles_graph(42, 29, edge_labels=("c", "d"))
    save_graph_to_file(g, os.sep.join(["..", "output", "exp-graph"]))
    print(get_info(g))
