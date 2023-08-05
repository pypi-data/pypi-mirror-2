"""str verus bytes"""

from six import _util

from six.const import PY3


if PY3:
    def b(s):
        return s.encode("latin-1")
    def u(s):
        return s
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO
else:
    def b(s):
        return s
    def u(s):
        return unicode(s)
    import StringIO
    StringIO = BytesIO = StringIO.StringIO
_util.add_doc(b, """Byte literal""")
_util.add_doc(u, """Text literal""")
