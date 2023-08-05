# -*- coding: utf-8 -*-
"""
    flaskext.creole
    ~~~~~~~~~~~~~~~

    Template filters and helpers for the creole parsers.

    :copyright: (c) 2010 by Ali Afshar.
    :license: MIT, see LICENSE for more details.
"""

from creoleparser.dialects import creole11_base, create_dialect
from creoleparser.core import Parser
from creoleparser import parse_args



class Creole(object):
    """Flask extension to add template filters for using creole

    :param app: The flask application
    :param dialect_base: The creoleparser dialect base to use (default
                         creole11_base)
    :param parser_method: The parser_method to use (default 'xml')
    :param dialect_kw: Keyword arguments passed to the dialect on instantiation.
    """

    def __init__(self, app, dialect_base=creole11_base,
                 parser_method='xml', **dialect_kw):
        self.macros = {}
        self.dialect = create_dialect(dialect_base,
                                      macro_func=self.dispatch_macro,
                                      **dialect_kw)
        self.creole = Parser(dialect=self.dialect, method=parser_method)
        app.jinja_env.filters['creole2html'] = self.creole2html


    def creole2html(self, markup):
        """Convert creole markup to html

        :param markup: The creole markup to convert to html.
        """
        return self.creole(markup)

    def add_macro(self, name, func):
        """Add a named macro to the macros.

        :param name: The name of the macro
        :param func: The macro handler function (see macro docstring for
                     definition of the handler function signature).
        """
        self.macros[name] = func

    def macro(self, func_or_name=None):
        """Decorator to define a function as a creole macro.

        The function should take the signature::

            def macro_function(name, environ, body, is_block, *args, **kw):
                ...

        name:
            The name used to call the macro.
        environ:
            The Creoleparser environment object
        body:
            The contents of the macro
        is_block:
            Whether the macro has been called as a block macro or an inline
            macro.

        Where ``*args`` and ``**kw`` can be replaced by specific macro argument
        names, or omitted entirely if the macro has no arguments.

        This decorator may be called with a name to use for the macro, and if
        omitted the decorated function name will be used instead.

        All the following are acceptable::
            
            creole = Creole(app)

            @creole.macro
            def macro_function(name, environ, body, is_block, *args, **kw):
                ...

            @creole.macro('my_macro_name')
            def macro_function(name, environ, body, is_block, *args, **kw):
                ...
            
            @creole.macro()
            def macro_function(name, environ, body, is_block, *args, **kw):
                ...
        """
        if callable(func_or_name):
            self.add_macro(func_or_name.__name__, func_or_name)
            return func_or_name
        else:
            def decorator(func, func_or_name=func_or_name):
                name = func_or_name or func.__name__
                self.add_macro(name, func)
                return func
            return decorator

    def dispatch_macro(self, macro_name, arg_string, body, is_block, environ):
        """Dispatch a macro.

        Called internally, usually.
        """
        macro = self.macros.get(macro_name)
        if macro is not None:
            args, kw = parse_args(arg_string)
            return macro(macro_name, environ, body, is_block, *args, **kw)

        


