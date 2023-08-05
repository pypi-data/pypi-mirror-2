#! /usr/bin/env python
import os
import sys

extra = {}
try:
    import setuptools
    from setuptools import setup
    setuptools.use_2to3_on_doctests = False
    extra['use_2to3'] = True
except ImportError:
    from distutils.core import setup

# attempt to get the metadata from the module - this won't work if the
# module hasn't been 2to3'ed yet as part of a "python3 setup.py build"
if sys.version_info >= (3,) and os.path.exists('build/lib/html.py'):
    sys.path.insert(0, 'build/lib')
try:
    from html import __version__, __doc__
except SyntaxError:
    # fallback just to get things moving
    __version__ = '1.9'
    __doc__ = 'docs'

# forge the PyPI description using the module doc with some installation
# instructions prepended
description = '''Installation
------------

Under Python 2 you should just ``python setup.py install`` but under Python
3 you will need to ``python3 setup.py build install`` -- note the
additional **build** command.

To support installation under both Python 2 and 3 the `distribute`_ package is
required.

.. _`distribute`: http://pypi.python.org/pypi/distribute#installation-instructions

''' + '\n'.join(__doc__.splitlines()[1:])


# perform the setup action
setup(
    name = "html",
    version = __version__,
    description = "simple, elegant HTML/XHTML generation",
    long_description = description,
    author = "Richard Jones",
    author_email = "rjones@ekit-inc.com",
    py_modules = ['html'],
    url = 'http://pypi.python.org/pypi/html',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: BSD License',
    ],
    **extra
)

# vim: set filetype=python ts=4 sw=4 et si
