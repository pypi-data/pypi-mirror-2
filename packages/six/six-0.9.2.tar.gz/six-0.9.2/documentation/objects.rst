Object Model Compatibility
==========================

.. module:: six.objects
   :synopsis: Object model compatibility

Python 3 renamed the attributes of several intepreter data structures.  This
module provides compatibility assessors.  Note that the recommended way to
inspect functions and methods is the stdlib :mod:`py3:inspect` module.


.. function:: get_unbound_function(meth)

   Get the function out of unbound method *meth*.  In Python 3, unbound methods
   don't exist, so this function just returns *meth* unchanged.  Example
   usage:::

      from six.objects import get_unbound_function
      class X(object):
          def method(self):
              pass
      method_function = get_unbound_function(X.method)


.. function:: get_method_function(meth)

   Get the function out of method object *meth*.


.. function:: get_method_self(meth)

   Get the ``self`` of bound method *meth*.


.. function:: get_function_code(func)

   Get the code object associated with *func*.


.. function:: get_function_defaults(func)

   Get the defaults tuple associated with *func*.


.. function:: advance_iterator(it)

   Get the next item of *it* and raise :exc:`StopIteration` if it had ended.
   This is a replacement for calling ``it.next()`` in Python 2 and ``next(it)``
   in Python 3.


.. function:: callable(obj)

   Check if *obj* can be called.
