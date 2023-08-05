"""
Flask Creole
------------

Description goes here...

Links
`````

* `documentation <http://packages.python.org/Flask%20Creole>`_
* `development version
  <http://bitbucket.org/USERNAME/REPOSITORY/get/tip.gz#egg=Flask%20Creole-dev>`_


"""
from setuptools import setup


setup(
    name='Flask-Creole',
    version='0.4.1',
    url='http://bitbucket.org/aafshar/flask-creole-main',
    license='MIT',
    author='Ali Afshar',
    author_email='aafshar@gmail.com',
    description='Creole parser filters for Flask',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'creoleparser'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
