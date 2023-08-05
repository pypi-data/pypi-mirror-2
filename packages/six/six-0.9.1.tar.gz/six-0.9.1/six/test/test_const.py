import sys
import operator

import py

from six import const, strdata


def test_integer_types():
    assert isinstance(1, const.integer_types)
    assert isinstance(-1, const.integer_types)
    assert isinstance(const.MAXSIZE + 23, const.integer_types)
    assert not isinstance(.1, const.integer_types)


def test_string_types():
    assert isinstance("hi", const.string_types)
    assert isinstance(strdata.u("hi"), const.string_types)
    assert issubclass(const.text_type, const.string_types)


def test_class_types():
    class X:
        pass
    class Y(object):
        pass
    assert isinstance(X, const.class_types)
    assert isinstance(Y, const.class_types)
    assert not isinstance(X(), const.class_types)


def test_text_type():
    assert type(strdata.u("hi")) is const.text_type


def test_binary_type():
    assert type(strdata.b("hi")) is const.binary_type


def test_MAXSIZE():
    py.test.raises(OverflowError, operator.mul, [None], const.MAXSIZE + 1)
