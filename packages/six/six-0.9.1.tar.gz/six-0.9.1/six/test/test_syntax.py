import sys

import py

from six import const, syntax, moves, strdata


def test_exec_():
    def f():
        l = []
        syntax.exec_("l.append(1)")
        assert l == [1]
    f()
    ns = {}
    syntax.exec_("x = 42", ns)
    assert ns["x"] == 42
    glob = {}
    loc = {}
    syntax.exec_("global y; y = 42; x = 12", glob, loc)
    assert glob["y"] == 42
    assert "x" not in glob
    assert loc["x"] == 12
    assert "y" not in loc


def test_reraise():
    def get_next(tb):
        if const.PY3:
            return tb.tb_next.tb_next
        else:
            return tb.tb_next
    e = Exception("blah")
    try:
        raise e
    except Exception:
        tp, val, tb = sys.exc_info()
    try:
        syntax.reraise(tp, val, tb)
    except Exception:
        tp2, value2, tb2 = sys.exc_info()
        assert tp2 is Exception
        assert value2 is e
        assert tb is get_next(tb2)
    try:
        syntax.reraise(tp, val)
    except Exception:
        tp2, value2, tb2 = sys.exc_info()
        assert tp2 is Exception
        assert value2 is e
        assert tb2 is not tb
    try:
        syntax.reraise(tp, val, tb2)
    except Exception:
        tp2, value2, tb3 = sys.exc_info()
        assert tp2 is Exception
        assert value2 is e
        assert get_next(tb3) is tb2


def test_print_():
    save = sys.stdout
    out = sys.stdout = moves.StringIO()
    try:
        syntax.print_("Hello,", "person!")
    finally:
        sys.stdout = save
    assert out.getvalue() == "Hello, person!\n"
    out = moves.StringIO()
    syntax.print_("Hello,", "person!", file=out)
    assert out.getvalue() == "Hello, person!\n"
    out = moves.StringIO()
    syntax.print_("Hello,", "person!", file=out, end="")
    assert out.getvalue() == "Hello, person!"
    out = moves.StringIO()
    syntax.print_("Hello,", "person!", file=out, sep="X")
    assert out.getvalue() == "Hello,Xperson!\n"
    out = moves.StringIO()
    syntax.print_(strdata.u("Hello,"), strdata.u("person!"), file=out)
    result = out.getvalue()
    assert isinstance(result, const.text_type)
    assert result == strdata.u("Hello, person!\n")
    syntax.print_("Hello", file=None) # This works.
    out = moves.StringIO()
    syntax.print_(None, file=out)
    assert out.getvalue() == "None\n"


def test_print_exceptions():
    py.test.raises(TypeError, syntax.print_, x=3)
    py.test.raises(TypeError, syntax.print_, end=3)
    py.test.raises(TypeError, syntax.print_, sep=42)


def test_with_metaclass():
    class Meta(type):
        pass
    class X(syntax.with_metaclass(Meta)):
        pass
    assert type(X) is Meta
    assert issubclass(X, object)
    class Base(object):
        pass
    class X(syntax.with_metaclass(Meta, Base)):
        pass
    assert type(X) is Meta
    assert issubclass(X, Base)
