Renamed modules and attributes compatibility
============================================

.. module:: six.moves
   :synopsis: Renamed modules and attributes compatibility


Python 3 reorganized the standard library and moved several functions to
different modules.  This module provides a consistent interface to them.  For
example, to load the module for parsing HTML on Python 2 or 3, write::

   from six.moves import html_parser

Similarly, to get the function to reload modules, which was moved from the
builtin module to the ``imp`` module, use::

   from six.moves import reload_module

For the most part, :mod:`six.moves` aliases are the names of the modules in
Python 3.  When the new Python 3 name is a package, the components of the name
are separated by underscores.  For example, ``html.parser`` because
``html_parser``.  In some cases where several modules have been combined, the
Python 2 name is retained.  This is so the appropiate modules can be found when
running on Python 2.  For example, ``BaseHTTPServer`` which is in
``http.server`` in Python 3 is aliased as ``BaseHTTPServer``.

Some modules which had two implementations have been merged in Python 3.  For
example, ``cPickle`` no longer exists in Python 3.  It's been merged with
``pickle``.  In these cases, fetching the fast version will load the fast one on
Python 2 and the merged module in Python 3.


.. note::

   The :mod:`py2:urllib`, :mod:`py2:urllib2`, and :mod:`py2:urlparse` modules
   have been combined in the :mod:`py3:urllib` package in Python 3.
   :mod:`six.moves` doesn't not support their renaming because their members
   have been mixed across several modules in that package.

Supported renames:

+------------------------------+-------------------------------------+---------------------------------+
| Name                         | Python 2 name                       | Python 3 name                   |
+==============================+=====================================+=================================+
| ``builtins``                 | :mod:`py2:__builtin__`              | :mod:`py3:builtins`             |
+------------------------------+-------------------------------------+---------------------------------+
| ``configparser``             | :mod:`py2:ConfigParser`             | :mod:`py3:configparser`         |
+------------------------------+-------------------------------------+---------------------------------+
| ``copyreg``                  | :mod:`py2:copy_reg`                 | :mod:`py3:copyreg`              |
+------------------------------+-------------------------------------+---------------------------------+
| ``cPickle``                  | :mod:`py2:cPickle`                  | :mod:`py3:pickle`               |
+------------------------------+-------------------------------------+---------------------------------+
| ``cStringIO``                | :func:`py2:cStringIO.StringIO`      | :class:`py3:io.StringIO`        |
+------------------------------+-------------------------------------+---------------------------------+
| ``http_cookiejar``           | :mod:`py2:cookielib`                | :mod:`py3:http.cookiejar`       |
+------------------------------+-------------------------------------+---------------------------------+
| ``http_cookies``             | :mod:`py2:Cookie`                   | :mod:`py3:http.cookies`         |
+------------------------------+-------------------------------------+---------------------------------+
| ``html_entities``            | :mod:`py2:htmlentitydefs`           | :mod:`py3:html.entities`        |
+------------------------------+-------------------------------------+---------------------------------+
| ``html_parser``              | :mod:`py2:HTMLParser`               | :mod:`py3:html.parser`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``http_client``              | :mod:`py2:httplib`                  | :mod:`py3:http.client`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``BaseHTTPServer``           | :mod:`py2:BaseHTTPServer`           | :mod:`py3:http.server`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``CGIHTTPServer``            | :mod:`py2:CGIHTTPServer`            | :mod:`py3:http.server`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``SimpleHTTPServer``         | :mod:`py2:SimpleHTTPServer`         | :mod:`py3:http.server`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``queue``                    | :mod:`py2:Queue`                    | :mod:`py3:queue`                |
+------------------------------+-------------------------------------+---------------------------------+
| ``reduce``                   | :func:`py2:reduce`                  | :func:`py3:functools.reduce`    |
+------------------------------+-------------------------------------+---------------------------------+
| ``reload_module``            | :func:`py2:reload`                  | :func:`py3:imp.reload`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``reprlib``                  | :mod:`py2:repr`                     | :mod:`py3:reprlib`              |
+------------------------------+-------------------------------------+---------------------------------+
| ``socketserver``             | :mod:`py2:SocketServer`             | :mod:`py3:socketserver`         |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter``                  | :mod:`py2:Tkinter`                  | :mod:`py3:tkinter`              |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_dialog``           | :mod:`py2:Dialog`                   | :mod:`py3:tkinter.dialog`       |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_filedialog``       | :mod:`py2:FileDialog`               | :mod:`py3:tkinter.FileDialog`   |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_scrolledtext``     | :mod:`py2:ScrolledText`             | :mod:`py3:tkinter.scolledtext`  |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_simpledialog``     | :mod:`py2:SimpleDialog`             | :mod:`py2:tkinter.simpledialog` |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_tix``              | :mod:`py2:Tix`                      | :mod:`py3:tkinter.tix`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_constants``        | :mod:`py2:Tkconstants`              | :mod:`py3:tkinter.constants`    |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_dnd``              | :mod:`py2:Tkdnd`                    | :mod:`py3:tkinter.dnd`          |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_colorchooser``     | :mod:`py2:tkColorChooser`           | :mod:`py3:tkinter.colorchooser` |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_commondialog``     | :mod:`py2:tkCommonDialog`           | :mod:`py3:tkinter.commondialog` |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_tkfiledialog``     | :mod:`py2:tkFileDialog`             | :mod:`py3:tkinter.filedialog`   |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_font``             | :mod:`py2:tkFont`                   | :mod:`py3:tkinter.font`         |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_messagebox``       | :mod:`py2:tkMessageBox`             | :mod:`py3:tkinter.messagebox`   |
+------------------------------+-------------------------------------+---------------------------------+
| ``tkinter_tksimpledialog``   | :mod:`py2:tkSimpleDialog`           | :mod:`py3:tkinter.simpledialog` |
+------------------------------+-------------------------------------+---------------------------------+
| ``urllib_robotparser``       | :mod:`py2:robotparser`              | :mod:`py3:urllib.robotparser`   |
+------------------------------+-------------------------------------+---------------------------------+
| ``winreg``                   | :mod:`py2:_winreg`                  | :mod:`py3:winreg`               |
+------------------------------+-------------------------------------+---------------------------------+
