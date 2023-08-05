import sys

from six import const, moves, _moves


def test_lazy():
    if const.PY3:
        html_name = "html.parser"
    else:
        html_name = "HTMLParser"
    assert html_name not in sys.modules
    mod = moves.html_parser
    assert sys.modules[html_name] is mod
    assert "htmlparser" not in _moves.MovedItems.__dict__


def pytest_generate_tests(metafunc):
    if "item_name" in metafunc.funcargnames:
        for value in _moves.attributes:
            if value.name == "winreg" and not sys.platform.startswith("win"):
                continue
            metafunc.addcall({"item_name" : value.name})


def test_items(item_name):
    """Ensure that everything loads correctly."""
    getattr(moves, item_name)
