#!/usr/bin/env python

from distutils.core import setup
import os

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme).read()

setup(name = 'computil',
        version = '0.01',
        description = 'Utilities for long-running computations.',
        author = 'Konrad Delong',
        author_email = 'konryd@gmail.com',
        url = 'http://github.com/konryd/computil',
        classifiers = [
              'Programming Language :: Python :: 2',
           ],
        py_modules = ['computil'],
        )
