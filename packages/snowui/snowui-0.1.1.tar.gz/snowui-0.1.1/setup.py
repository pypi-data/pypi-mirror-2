from setuptools import setup, find_packages
from setuptools.extension import Extension as BaseExtension
import re

import sys, os


long_description = open("README").read() + """

Changelog
=========

""" + open("CHANGELOG").read()

version = re.search('__version__ = "([0-9\.a-z]+)"',
        open("snowui/__init__.py").read()).groups()[0]

setup(
    name = 'snowui',
    version = version,
    author = "Joey Marshall",
    author_email = "joey@joey101.net",
    description = "snowui is a fast and simple GUI using pyglet and rabbyt.",
    license = "MIT",
    url="http://joey101.net/snowui/",
    long_description=long_description,

    packages = find_packages(),
    include_package_data = True,
    exclude_package_data = {'':['README', 'examples', 'docs']},
)
