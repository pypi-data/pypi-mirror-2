#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Bradford A Toney on 2010-06-27.
"""

import os, sys
import time, glob
from setuptools import setup, find_packages, Extension

extensions = [
    Extension('common.mm_hash', ['src/mm_hash.c']),    
]

setup(
    name = 'bm_common',
    version = '0.0.1b',
    author = 'Alex Toney',
    author_email = "toneyalex@gmail.com",
    description = "This is shared code between projects",
    license = "GPL",
    keywords = "misc utils extra",
    packages=['bm_common', 'bm_common.maths'],
    package_dir = {'bm_common': 'src'},
    ext_modules = extensions,
    zip_safe=False,
    test_suite = 'nose.collector',
    setup_requires = ['nose>=0.10.4'],
    entry_points = {}
)