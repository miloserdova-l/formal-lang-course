from pyformlang.finite_automaton import FiniteAutomaton, State
from scipy.sparse import kron, dok_matrix, bsr_matrix


def get_edges_by_label(fa: FiniteAutomaton) -> tuple[dict[str, dok_matrix], dict]:
    n = len(fa.states)
    edges = fa.to_dict()
    d = dict()
    node_number = dict()
    state_by_number = dict()

    def get_node_number(x: State) -> int:
        if x not in node_number.keys():
            state_by_number[len(node_number)] = x
            node_number[x] = len(node_number)
        return node_number.get(x)

    for u in edges.keys():
        i = get_node_number(u)
        for label in edges.get(u).keys():
            if not isinstance(edges.get(u).get(label), set):
                edges.get(u)[label] = {edges.get(u).get(label)}
            for v in edges.get(u).get(label):
                j = get_node_number(v)
                if label not in d.keys():
                    d[label] = dok_matrix((n, n), dtype=bool)
                d[label][i, j] = True
    return d, state_by_number


def get_intersection(
    g: FiniteAutomaton, r: FiniteAutomaton
) -> tuple[bsr_matrix, dict, dict]:
    g_edges, state_by_number_g = get_edges_by_label(g)
    r_edges, state_by_number_r = get_edges_by_label(r)
    n = len(g.states)
    m = len(r.states)
    labels = g.symbols.intersection(r.symbols)
    b = bsr_matrix((n * m, n * m), dtype=bool)
    for label in labels:
        b += kron(g_edges[label], r_edges[label])
    return b, state_by_number_g, state_by_number_r


def transitive_closure(m: bsr_matrix) -> bsr_matrix:
    while True:
        old = m.todense().tolist()
        m += m.dot(m)
        new = m.todense().tolist()
        if new == old:
            break
    return m


def rpq(g: FiniteAutomaton, r: FiniteAutomaton) -> set:
    k, state_by_number_g, state_by_number_r = get_intersection(g, r)
    tc = transitive_closure(k)
    x, y = tc.nonzero()
    ans = set()
    for (i, j) in zip(x, y):
        a = i // len(r.states)
        b = j // len(r.states)
        if (
            state_by_number_g.get(a) in g.start_states
            and state_by_number_g.get(b) in g.final_states
            and state_by_number_r.get(i % len(r.states)) in r.start_states
            and state_by_number_r.get(j % len(r.states)) in r.final_states
        ):
            ans.add((a, b))
    return ans
