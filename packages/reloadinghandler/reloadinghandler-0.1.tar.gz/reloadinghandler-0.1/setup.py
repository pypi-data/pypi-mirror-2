#!/usr/bin/python

# from distutils.core import setup
from setuptools import setup, find_packages

setup(name="reloadinghandler",
      version="0.1",
      description="A HTTP request handler shim",
      author="Michael Wolf",
      author_email="maw@pobox.com",
      keywords="http testing",
      py_modules=["ReloadingHandler"],)
