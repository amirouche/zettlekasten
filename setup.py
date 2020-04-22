#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="zettlekasten",
    version="0.0.2",
    author="Amirouche BOUBEKKI",
    author_email="amirouche@hyper.dev",
    url="https://github.com/amirouche/zettlekasten",
    description="Zettlekasten at its finest!",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',  # This is important!
    py_modules=['zettlekasten'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
