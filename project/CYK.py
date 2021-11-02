from itertools import product

from pyformlang.cfg import Terminal, CFG


def cyk(s: list[Terminal], cnf: CFG):
    if not cnf.remove_epsilon().is_normal_form():
        raise ValueError("Grammar should be converted to Chomsky Normal Form")
    n = len(s)

    if n == 0:
        return cnf.generate_epsilon()

    heads = dict()

    for p in cnf.productions:
        if len(p.body) == 1:
            body = p.body[0]
        else:
            body = tuple(p.body)
        heads[body] = heads.get(body, set()) | {p.head}

    # substring s[i]...s[j] is derived from set equal to dp[i][j]
    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        dp[i][i] |= heads.get(s[i], set())

    for length in range(1, n):
        for i in range(n - length):
            for k in range(i, i + length):
                for first, second in product(dp[i][k], dp[k + 1][i + length]):
                    dp[i][i + length] |= heads.get((first, second), set())

    return cnf.start_symbol in dp[0][n - 1]
