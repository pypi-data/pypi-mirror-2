"""Utilities for writing code that runs on Python 2 and 3"""

__version__ = "0.9.2"

import sys

from six.const import PY3

from six._moves import moves
sys.modules["six.moves"] = moves
