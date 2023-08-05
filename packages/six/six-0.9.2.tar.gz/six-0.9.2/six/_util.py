"""Internal utilities"""

import sys


def add_doc(func, doc):
    """Add documentation to a function."""
    func.__doc__ = doc


def import_module(name):
    """Import module, returning last module in string."""
    __import__(name)
    return sys.modules[name]
