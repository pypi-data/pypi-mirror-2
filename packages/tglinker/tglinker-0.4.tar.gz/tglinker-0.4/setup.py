# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='tglinker',
    version='0.4',
    description='TurboGears EC2 symlink Generation Tool',
    author='Michael J. Pedersen',
    author_email='m.pedersen@icelus.org',
    py_modules=['tglinker'],
    entry_points="""
    [console_scripts]
    tglinker = tglinker:main
    """,
)
