#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    setup_requires=['d2to1'],
    d2to1=True,
    namespace_packages=['stsci'], packages=['stsci'],
    use_2to3=True,
    zip_safe=False
)
