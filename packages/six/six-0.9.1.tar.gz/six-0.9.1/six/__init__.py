"""Utilities for writing code that runs on Python 2 and 3"""

__version__ = "0.9.1"

import sys

from .const import PY3

from ._moves import moves
sys.modules["six.moves"] = moves
