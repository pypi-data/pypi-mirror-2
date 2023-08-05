
from flask import Flask, render_template_string

from flaskext.creole import Creole

markup = u'This is **creole //markup//**'
macro_markup = "<<hello some_arg='ali'>>"
macro_markup2 = "<<hello3>>"
html = u'<p>This is <strong>creole <em>markup</em></strong></p>\n'
html_pc = u'<p>This is <strong>creole <i>markup</i></strong></p>\n'
macro_html = '<p>Hello World ali</p>\n'
macro_html2 = '<p>Hello</p>\n'


def create_client(Creole=Creole):
    app = Flask(__name__)
    app.debug = True
    creole = Creole(app)

    @app.route('/c2h')
    def view_creole2html():
        return render_template_string('{{ markup|creole2html }}', markup=markup)

    @app.route('/m')
    def view_creole_macro():
        return render_template_string('{{ markup|creole2html }}',
                                      markup=macro_markup)

    @app.route('/m2')
    def view_creole_macro2():
        return render_template_string('{{ markup|creole2html }}',
                                      markup=macro_markup2)

    @creole.macro
    def hello(name, environ, body, is_block, some_arg):
        return 'Hello World %s' % (some_arg)

    @creole.macro('hello3')
    def hello2(name, environ, body, is_block):
        return 'Hello'

    print creole.macros
        


    return app.test_client()


def test_creole_to_html_cp():
    client = create_client()
    resp = client.open('/c2h')
    assert resp.data == html


def test_macro():
    client = create_client()
    resp = client.open('/m')
    print resp.data
    assert resp.data == macro_html
    
def test_named_macro():
    client = create_client()
    resp = client.open('/m2')
    assert resp.data == macro_html2
    

