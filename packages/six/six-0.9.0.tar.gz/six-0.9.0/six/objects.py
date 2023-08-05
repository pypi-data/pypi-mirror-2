"""Object model compatibility"""

from . import _util

from .const import PY3


if PY3:
    _meth_func = "__func__"
    _meth_self = "__self__"

    _func_code = "__code__"
    _func_defaults = "__defaults__"
else:
    _meth_func = "im_func"
    _meth_self = "im_self"

    _func_code = "func_code"
    _func_defaults = "func_defaults"


if PY3:
    def get_unbound_function(unbound):
        return unbound
else:
    def get_unbound_function(unbound):
        return unbound.im_func
_util.add_doc(get_unbound_function,
              """Get the function out of a possibly unbound function""")


def get_method_function(meth):
    """Get the underlying function of a bound method."""
    return getattr(meth, _meth_func)


def get_method_self(meth):
    """Get the self of a bound method."""
    return getattr(meth, _meth_self)


def get_function_code(func):
    """Get code object of a function."""
    return getattr(func, _func_code)


def get_function_defaults(func):
    """Get defaults of a function."""
    return getattr(func, _func_defaults)
