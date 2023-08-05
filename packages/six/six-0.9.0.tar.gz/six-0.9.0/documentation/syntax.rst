Syntax compatibility
====================

.. module:: six.syntax
   :synopsis: Syntax compatibility helpers


This module provides functions for actions for which different versions of
Python have different syntax.


.. function:: exec_(code, globals=None, locals=None)

   Execute *code* in the scope of *globals* and *locals*.  *code* can be a
   string or a code object.  If *globals* or *locals* is not given, they will
   default to the scope of the caller.  If just *globals* is given, it will also
   be used as *locals*.


.. function:: print_(*args, *, file=sys.stdout, end="\n", sep=" ")

   Print *args* into *file*.  Each argument will be separated with *sep* and
   *end* will be written to the file at the last.

   .. note::

      In Python 2, this function imitates Python 3's :func:`py3:print` but not
      having softspace support.  If you don't know what that is, you're probably
      ok. :)


.. function:: reraise(exc_type, exc_value, exc_traceback=None)

   Reraise an exception, possibly with a different traceback.  In the simple
   case, ``reriase(*sys.exc_info())`` with an active exception (in an except
   block) reraises the current exception with the last traceback.  A different
   traceback can be specified with the *exc_traceback* parameter.


.. function:: with_metaclass(metaclass, base=object)

   Create a new class with base class *base* and metaclass *metaclass*.  This is
   designed to be used in class declarations like this: ::

      from six.syntax import with_metaclass

      class Meta(type):
          pass

      class Base(object):
          pass

      class MyClass(with_metaclass(Meta, Base)):
          pass
