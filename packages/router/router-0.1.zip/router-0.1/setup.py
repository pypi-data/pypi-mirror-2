# -*- coding: utf-8 -*-
"""
router
~~~~~~

router is a simple yet extensible URL routing library for Python.

It is derived from the routing mechanism implemented for `webapp2 <http://code.google.com/p/webapp-improved/>`_.

Repository: http://code.google.com/p/url-router/
"""
from setuptools import setup

setup(
    name = 'router',
    version = '0.1',
    license = 'Apache Software License',
    url = 'http://www.tipfy.org/',
    description = "A simple yet extensible URL routing library for Python",
    long_description = __doc__,
    author = 'Rodrigo Moraes',
    author_email = 'rodrigo.moraes@gmail.com',
    zip_safe = False,
    platforms = 'any',
    py_modules=['router'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)