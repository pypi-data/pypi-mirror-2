Binary and Text Data Handling
=============================

.. module:: six.strdata
   :synopsis: Tools for separating string types

Python 3 enforces the distinction between far more rigoriously than does Python
2; binary data cannot be automatically coerced text data.  six provides the
several functions to assist in classifying string data in all Python versions.


.. function:: b(data)

   A "fake" bytes literal.  *data* should always be a normal string literal.  In
   Python 2, :func:`b` returns :func:`py2:str`.  In Python 3, *data* is encoded
   with the latin-1 encoding to :func:`py3:bytes`.


.. function:: u(text)

   A "fake" unicode literal.  *text* should always be a normal string literal.
   In Python 2, :func:`u` returns :func:`py2:unicode`, and in Python 3,
   :func:`py3:str`.


.. data:: StringIO

   This is an fake file object for textual data.  It's an alias for
   :class:`py2:StringIO.StringIO` in Python 2 and :class:`py3:io.StringIO` in
   Python 3.


.. data:: BytesIO

   This is a fake file object for binary data.  In Python 2, it's an alias for
   :class:`py2:StringIO.StringIO`, but in Python 3, it's an alias for
   :class:`py3:io.BytesIO`.
