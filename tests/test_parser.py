import pytest
import platform

if platform.system() == "Windows":
    pytest.skip("skipping", allow_module_level=True)
else:
    from project.gql.parser import parse


@pytest.mark.parametrize(
    "text, accept",
    [
        ("_secret_graph", True),
        ("FirstGraph", True),
        ("1stGraph", False),
        ("!graph", False),
    ],
)
def test_var(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.var()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("true", True),
        ("false", True),
        ("True", False),
        ("False", False),
        ("T", False),
        ("F", False),
        ("1", True),
        ("100", True),
        ('"I hate this"', True),
        ("I hate this", False),
    ],
)
def test_val(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.val()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("set start of g to {1..10}", True),
        ("set start of g to {1...10}", False),
        ("set final of g to {1..10}", True),
        ("add start of g to {1, 2, 3}", True),
        ("add final of g to labels1", True),
        ("add final of g {1, 5, 3, 2, 4}", False),
        ('load graph "/home"', True),
        (
            '''"""
            S -> A B
            A -> A a | a
            B -> B b | b
        """''',
            True,
        ),
    ],
)
def test_graph(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.graph()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("1", True),
        ("{1..10}", True),
        ("get vertices from g", True),
        ("get start vertices from g", True),
        ("get reachable vertices from g", True),
        ("get from g", False),
    ],
)
def test_vertices(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.vertices()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ('(1, "a", 2)', True),
        ('("1", "a", "2")', False),
        ("{(1, 2), (3, 4), (5, 6)}", True),
        ("{(1, 2), ('a', 4), (5, 6)}", False),
        ("get edges from g", True),
        ("get edges from 1", False),
        ("get start from 1", False),
    ],
)
def test_edges(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.edges()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("get labels from g", True),
        ('"label"', True),
        ("label", False),
        ('{"l1", "l2"}', True),
        ('{"l1", l2}', False),
    ],
)
def test_labels(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.labels()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("map (fun x: x) g", True),
        ("map (fun ((u,v),l,(w,q)): g) " "(get edges from res1)", True),
        ("map (fun 1: 1) 1", False),
        ("map map map", False),
    ],
)
def test_map(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.mapping()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("filter (fun x: x) g", True),
        (
            "filter (fun ((u,v),l,(w,q)): g) (get edges from res1)",
            True,
        ),
        (" filter (fun 1: 1) 1", False),
        ("filter p p", False),
    ],
)
def test_filter(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.filtering()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("fun x,y,z: x", True),
        ("fun v: v in s", True),
        ("fun ((u,v),l,(w,q)) : g", True),
        ("fun {x, y, z} : 1", False),
        ("fun 1, 2, 3: 1", False),
    ],
)
def test_lambda(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.anfunc()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("not g1 & g2", True),
        ("g1", True),
        ("{2..100} & {1}", True),
        ("", False),
        ("(get edges from g) & {(1, 2)}", True),
        ("(get from g) & {(1, 2)}", False),
        ("filter (fun (x, y): x in s) g", True),
    ],
)
def test_expr(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.expr()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("print g2", True),
        ("println(g2)", False),
        ("print {1..100}", True),
        ("print", False),
        ('g1 = load graph "wine"', True),
        ("g1 = load graph", False),
        ("g1 = {1..100}", True),
    ],
)
def test_stmt(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.stmt()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        (
            """
            g = load graph "wine";
            h = set start of (set final of g to (get vertices from g)) to {1..100};
            l1 = "l1" | "l2";
            q1 = ("type" | l1)*;
            q2 = "sub_class_of" . l1;
            res1 = intersect g with q1;
            res2 = intersect g with q2;
            print res1;
            s = get start vertices from g;
            v = filter (fun v : v in s) (get edges from res1);
            print v;
            """,
            True,
        ),
        ('g = load graph "wine"', False),
        ('g = load graph "wine";', True),
    ],
)
def test_prog(text, accept):
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.prog()
    act = parser.getNumberOfSyntaxErrors() == 0
    assert act == accept
