from six import _util


def test_add_doc():
    def f():
        """Icky doc"""
        pass
    _util.add_doc(f, """New doc""")
    assert f.__doc__ == "New doc"


def test_import_module():
    m = _util.import_module("six._util")
    assert m is _util
