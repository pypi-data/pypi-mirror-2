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
    py.test.raises(AttributeError, objects.get_method_function, hasattr)


def test_get_function_code():
    def f():
        pass
    assert isinstance(objects.get_function_code(f), types.CodeType)
    py.test.raises(AttributeError, objects.get_function_code, hasattr)


def test_get_function_defaults():
    def f(x, y=3, b=4):
        pass
    assert objects.get_function_defaults(f) == (3, 4)


def test_advance_iterator():
    l = [1, 2]
    it = iter(l)
    assert objects.advance_iterator(it) == 1
    assert objects.advance_iterator(it) == 2
    py.test.raises(StopIteration, objects.advance_iterator, it)
    py.test.raises(StopIteration, objects.advance_iterator, it)


def test_callable():
    class X:
        def __call__(self):
            pass
        def method(self):
            pass
    assert objects.callable(X)
    assert objects.callable(X())
    assert objects.callable(test_callable)
    assert objects.callable(hasattr)
    assert objects.callable(X.method)
    assert objects.callable(X().method)
    assert not objects.callable(4)
    assert not objects.callable("string")
