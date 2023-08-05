#!/usr/bin/env python

from setuptools import setup
import os

try:
    fp = open(os.path.join(os.path.dirname(__file__), "README.rst"))
    readme_text = fp.read()
    fp.close()
except IOError:
    readme_text = fp.read()

setup(
    name='CleverCSS2',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    maintainer='Jared Forsyth',
    maintainer_email='jared@jaredforsyth.com',
    version='0.5',
    url='http://sandbox.pocoo.org/clevercss/',
    download_url='http://github.com/jabapyth/clevercss2',
    packages=['clevercss2'],
    description='python inspired sass-like css preprocessor',
    long_description=readme_text,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python'
    ],
    test_suite = 'tests.all_tests',
)
