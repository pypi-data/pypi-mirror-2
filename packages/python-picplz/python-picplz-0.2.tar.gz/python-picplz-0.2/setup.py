#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="python-picplz",
      version="0.2",
      description="Picplz library for Python",
      license="MIT",
      author="Jesse Emery",
      author_email="jesse@onagertech.com",
      url="http://github.com/ejesse/python-picplz",
      packages = ['picplz'],
      keywords= "picplz library",
      zip_safe = True)