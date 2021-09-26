import argparse
import sys
import cfpq_data
from pathlib import Path
import networkx.drawing.nx_pydot
from pyformlang.regular_expression import PythonRegex

from project.graph_utils import (
    get_info,
    create_labeled_two_cycles_graph,
    save_graph_to_file,
    graph_to_nfa,
)
from project.rpq import rpq
from project.regex_utils import regex_to_min_dfa


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()
    group = subparsers.add_parser(name="simple").add_mutually_exclusive_group(
        required=True
    )
    group.add_argument(
        "-print-graph-info",
        metavar="NAME",
        type=str,
        help="Prints graph info. Specify graph name as a parameter",
    )
    group.add_argument(
        "-gen-graph",
        nargs=5,
        metavar=(
            "FIRST_SIZE",
            "SECOND_SIZE",
            "FIRST_LABEL",
            "SECOND_LABEL",
            "OUTPUT_FILE",
        ),
        action="store",
        help="Generate two cycles graph.",
    )
    rpq_args = subparsers.add_parser(name="rpq")
    rpq_args.add_argument("-regex", type=str, action="store", required=True)
    rpq_args.add_argument(
        "-graph",
        type=str,
        action="store",
        help="Path to .dot file or graph name",
        required=True,
    )
    rpq_args.add_argument(
        "-start-nodes", nargs="+", metavar="START_NODE", action="store"
    )
    rpq_args.add_argument(
        "-final-nodes", nargs="+", metavar="FINAL_NODE", action="store"
    )
    args = parser.parse_args()
    if "print_graph_info" in args:
        if args.print_graph_info is not None:
            name = args.print_graph_info
            if all(
                name not in cfpq_data.DATASET[graph_class].keys()
                for graph_class in cfpq_data.DATASET.keys()
            ):
                print("No graph with such name", file=sys.stderr)
                exit(1)
            graph = cfpq_data.graph_from_dataset(name, verbose=False)
            print(get_info(graph))
        if args.gen_graph is not None:
            gen_graph_args = args.gen_graph
            if not (gen_graph_args[0].isdigit() and gen_graph_args[1].isdigit()):
                print("Size of cycles should be integer", file=sys.stderr)
                exit(1)
            n = int(gen_graph_args[0])
            m = int(gen_graph_args[1])
            labels = (gen_graph_args[2], gen_graph_args[3])
            output = gen_graph_args[4]
            save_graph_to_file(create_labeled_two_cycles_graph(n, m, labels), output)
    if "regex" in args:
        regex = regex_to_min_dfa(PythonRegex(args.regex))
        name = args.graph
        file = Path(name)
        if all(
            name not in cfpq_data.DATASET[graph_class].keys()
            for graph_class in cfpq_data.DATASET.keys()
        ):
            if not file.is_file():
                print("No graph with such name", file=sys.stderr)
                exit(1)
            else:
                graph = networkx.drawing.nx_pydot.read_dot(file)
        else:
            graph = cfpq_data.graph_from_dataset(name, verbose=False)
        for (u, v) in rpq(
            graph_to_nfa(graph, args.start_nodes, args.final_nodes), regex
        ):
            print("There is path between {} and {}".format(u, v))
