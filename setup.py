#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from version import __version__

setup(
    name='validator',
    version=__version__,
    description='A plain-as-vanilla validating package written for Python.',
    author='Wilhelm Murdoch',
    author_email='wilhelm.murdoch@gmail.com',
    url='http://www.devilmayco.de/',
    packages=find_packages(exclude=['tests', 'tests.*']),
    setup_requires=[
          'nose==1.3.0'
        , 'yanc==0.2.3'
    ]
)
