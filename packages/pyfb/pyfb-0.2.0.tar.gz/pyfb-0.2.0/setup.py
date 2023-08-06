#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='pyfb',
    version='0.2.0',
    description='A Python Interface to the Facebook Graph API',
    author='Juan Manuel García',
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Facebook Graph API Wrapper Python",
    url='http://code.google.com/p/pyfb/',
    package_dir={'': 'src'},
    py_modules=[
        'pyfb',
        'utils',
    ],
)
