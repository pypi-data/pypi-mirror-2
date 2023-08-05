
Flask Creole
============

Helpers and filters for Creole usage in Flask.

Quickstart
----------

Install::

    easy_install Flask-Creole

Code::

    hg clone http://bitbucket.org/aafshar/flask-creole-main

Usage as a template filter
--------------------------

Load the extension::

    from flaskext.creole import Creole
    creole = Creole(app)

Now in your templates you can use the filters::

    {{ article.body|creole2html }}


Usage outside templates
-----------------------

You can also use this functionality outside templates::

    from flaskext.creole import Creole
    creole = Creole(app)
    article.html = creole.creole2html(article.body)


Adding your own macros
----------------------

You can add your own macros to extend creoleparser.

Load the extension and declare the macro::

    from flaskext.creole import Creole
    creole = Creole(app)

    @creole.macro
    def hello(name, environ, body, is_block, *args, **kw):
        return 'Hello World'
    
Now use it in some markup::

    {{ '<<hello>>'|creole2html }}

API
---

.. autoclass:: flaskext.creole.Creole
    :members:

