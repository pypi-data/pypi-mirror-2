#! /usr/bin/env python
import os
import sys
import setuptools
from setuptools import setup

# attempt to get the metadata from the module - this won't work if the
# module hasn't been 2to3'ed yet as part of a "python3 setup.py build"
if sys.version_info >= (3,) and os.path.exists('build/lib/html.py'):
    sys.path.insert(0, 'build/lib')
try:
    from html import __version__, __doc__
except SyntaxError:
    __version__ = '1.9'
    __doc__ = 'docs'

setuptools.use_2to3_on_doctests = False

# perform the setup action
setup(
    name = "html",
    version = __version__,
    description = "simple, elegant HTML/XHTML generation",
    long_description = __doc__,
    author = "Richard Jones",
    author_email = "rjones@ekit-inc.com",
    py_modules = ['html'],
    use_2to3 = True,
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
)

# vim: set filetype=python ts=4 sw=4 et si
