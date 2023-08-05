#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

import jpath

setup(
    name='jpath',
    py_modules=['jpath'],
    version=jpath.__version__,
    description='Access nested dicts and lists using JSON-like path notation.',
    long_description=jpath.__doc__,
    author='Radomir Dopieralski',
    author_email='jpath@sheep.art.pl',
    classifiers = [
'Development Status :: 2 - Pre-Alpha',
'License :: OSI Approved :: Python Software Foundation License',
'Programming Language :: Python',
'Intended Audience :: Developers',
'License :: OSI Approved :: Python Software Foundation License',
'Operating System :: OS Independent',
'Topic :: Software Development :: Libraries :: Python Modules',
'Topic :: Text Processing',
    ],
)
