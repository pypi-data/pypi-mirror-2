# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension

setup(
    name='cxor',
    description='fast xor',
    version='0.1',
    author='Viktor Kotseruba',
    author_email='barbuzaster@gmail.com',
    license='MIT',
    keywords='web',
    url='http://bitbucket.org/barbuza/cxor/',
    ext_modules=[Extension('cxor', ['cxor.c'])]
)
