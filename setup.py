# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='wedNESday',
    version='0.0.1',
    description='wedNESday',
    long_description=long_description,
    author="Guto Maia",
    author_email="guto@guto.net",
    license="Mit",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "wednesday"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
    ]
)
