Constants
=========

.. module:: six.const
   :synopsis: Useful compatibility constants


This module contains constants that differ between Python versions.  Ones ending
``_types`` are mostly useful as the second argument to ``isinstance`` or
``issubclass``.


.. data:: class_types

   Possible class types.  In Python 2, this encompasses old-style and new-style
   classes.  In Python 3, this is just new-styles.


.. data:: integer_types

   Possible integer types.  In Python 2, this is :func:`py2:long` and
   :func:`py2:int`, and in Python 3, just :func:`py3:int`.


.. data:: string_types

   Possible types for text data.  This is :func:`py2:basestring` in Python 2 and
   :func:`py3:str` in Python 3.


.. data:: text_type

   Type for representing textual data in Unicode.  This is :func:`py2:unicode`
   in Python 2 and :func:`py3:str` in Python 3.


.. data:: binary_type

   Type for representing binary data.  This is :func:`py2:str` in Python 2 and
   :func:`py3:bytes` in Python 3.


.. data:: MAXSIZE

   The maximum size of a container.


Here's example usage of the module::

   from six import const

   def dispatch_types(value):
       if isinstance(value, const.integer_types):
           handle_integer(value)
       elif isinstance(value, const.class_types):
           handle_class(value)
       elif isinstance(value, const.string_types):
           handle_string(value)
