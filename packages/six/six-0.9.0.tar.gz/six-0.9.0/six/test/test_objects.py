import types

import py

from six import objects


def test_get_unbound_function():
    class X(object):
        def m(self):
            pass
    assert objects.get_unbound_function(X.m) is X.__dict__["m"]


def test_get_method_self():
    class X(object):
        def m(self):
            pass
    x = X()
    assert objects.get_method_self(x.m) is x
    py.test.raises(AttributeError, objects.get_method_self, 42)


def test_get_method_function():
    class X(object):
        def m(self):
            pass
    x = X()
    assert objects.get_method_function(x.m) is X.__dict__["m"]
    py.test.raises(AttributeError, objects.get_method_function, all)


def test_get_function_code():
    def f():
        pass
    assert isinstance(objects.get_function_code(f), types.CodeType)
    py.test.raises(AttributeError, objects.get_function_code, all)


def test_get_function_defaults():
    def f(x, y=3, b=4):
        pass
    assert objects.get_function_defaults(f) == (3, 4)
