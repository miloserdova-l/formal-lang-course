import pytest
import platform, os

if platform.system() == "Windows":
    pytest.skip("skipping", allow_module_level=True)
else:
    from project.gql.parser import generate_dot

from antlr4.error.Errors import ParseCancellationException


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_write_dot(tmpdir):
    text = """g = load graph "wine";
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
            """
    path = os.sep.join([root_path, "tests", "resources", "example.dot"])

    file = tmpdir.mkdir("test_dir").join("test.dot")
    generate_dot(text, file)

    with open(path, "r") as file1:
        with open(file, "r") as file2:
            assert file1.read() == file2.read()


def test_incorrect_text():
    text = """g = load graph "wine";
            h = set start of (set final of g to (get vetices from g)) to {1..100};
            l1 = "l1" | "l2";
            q1 = ("type" | l1)*;
            q2 = "sub_class_of" . l1;
            res1 = intersect g with q1;
            res2 = intersect g with q2;
            print res1;
            s = get start vertices from g;
            v = filter (fun v : v in s) (get edges from res1);
            print v;
            """
    with pytest.raises(ParseCancellationException):
        generate_dot(text, "test")
