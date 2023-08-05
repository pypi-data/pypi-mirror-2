"""Renamed modules and attributes"""

import types

from six import _util

from six.const import PY3


class _LazyDescr(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, tp):
        result = self._resolve()
        setattr(obj, self.name, result)
        # This is a bit ugly, but it avoids running this again.
        delattr(tp, self.name)
        return result


class _Module(_LazyDescr):

    def __init__(self, name, old, new=None):
        super(_Module, self).__init__(name)
        if PY3:
            if new is None:
                new = name
            self.mod = new
        else:
            self.mod = old

    def _resolve(self):
        return _util.import_module(self.mod)


class _Attribute(_LazyDescr):

    def __init__(self, name, old_mod, new_mod, old_attr=None, new_attr=None):
        super(_Attribute, self).__init__(name)
        if PY3:
            if new_mod is None:
                new_mod = name
            self.mod = new_mod
            if new_attr is None:
                if old_attr is None:
                    new_attr = name
                else:
                    new_attr = old_attr
            self.attr = new_attr
        else:
            self.mod = old_mod
            if old_attr is None:
                old_attr = name
            self.attr = old_attr

    def _resolve(self):
        module = _util.import_module(self.mod)
        return getattr(module, self.attr)



class MovedItems(types.ModuleType):
    """Lazy loading of moved objects"""


attributes = [
    _Attribute("cStringIO", "cStringIO", "io", "StringIO"),
    _Attribute("reload_module", "__builtin__", "imp", "reload"),
    _Attribute("reduce", "__builtin__", "functools"),
    _Attribute("StringIO", "StringIO", "io"),

    _Module("builtins", "__builtin__"),
    _Module("configparser", "ConfigParser"),
    _Module("copyreg", "copy_reg"),
    _Module("http_cookiejar", "cookielib", "http.cookiejar"),
    _Module("http_cookies", "Cookie", "http.cookies"),
    _Module("html_entities", "htmlentitydefs", "html.entities"),
    _Module("html_parser", "HTMLParser", "html.parser"),
    _Module("http_client", "httplib", "http.client"),
    _Module("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    _Module("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    _Module("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    _Module("cPickle", "cPickle", "pickle"),
    _Module("queue", "Queue"),
    _Module("reprlib", "repr"),
    _Module("socketserver", "SocketServer"),
    _Module("tkinter", "Tkinter"),
    _Module("tkinter_dialog", "Dialog", "tkinter.dialog"),
    _Module("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    _Module("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    _Module("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    _Module("tkinter_tix", "Tix", "tkinter.tix"),
    _Module("tkinter_constants", "Tkconstants", "tkinter.constants"),
    _Module("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    _Module("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser"),
    _Module("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog"),
    _Module("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    _Module("tkinter_font", "tkFont", "tkinter.font"),
    _Module("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    _Module("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog"),
    _Module("urllib_robotparser", "robotparser", "urllib.robotparser"),
    _Module("winreg", "_winreg"),
]
for attr in attributes:
    setattr(MovedItems, attr.name, attr)
del attr


moves = MovedItems("moves")
