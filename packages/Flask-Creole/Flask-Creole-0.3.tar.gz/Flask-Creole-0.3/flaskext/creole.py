# -*- coding: utf-8 -*-
"""
    flaskext.creole
    ~~~~~~~~~~~~~~~

    Template filters and helpers for the creole parsers.

    :copyright: (c) 2010 by Ali Afshar.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

try:
    from creoleparser.dialects import creole11_base, create_dialect
    from creoleparser.core import Parser
    from creoleparser import parse_args
    cp = True
except ImportError:
    cp = False

try:
    from creole import creole2html, html2creole
    pc = True
except ImportError:
    pc = False

if not (cp or pc):
    raise ImportError('One of creoleparser or python-creole need to be installed.')


class Creole_PC(object):

    def __init__(self, app):
        app.jinja_env.filters['creole2html'] = creole2html
        app.jinja_env.filters['html2creole'] = html2creole


class Creole_CP(object):
    """Flask extension to add template filters for using creole
    """

    def __init__(self, app, dialect_base=creole11_base,
                 parser_method='xml', **dialect_kw):
        self.macros = {}
        self.dialect = create_dialect(dialect_base,
                                      macro_func=self.dispatch_macro,
                                      **dialect_kw)
        self.creole = Parser(dialect=self.dialect, method=parser_method)
        app.jinja_env.filters['creole2html'] = self.creole

    def dispatch_macro(self, macro_name, arg_string, body, is_block, environ):
        macro = self.macros.get(macro_name)
        if macro is not None:
            args, kw = parse_args(arg_string)
            return macro(macro_name, environ, body, is_block, *args, **kw)

    def macro(self, f, name=None):
        name = name or f.__name__
        self.macros[name] = f
        return f

        
Creole = (cp and Creole_CP) or Creole_PC    


