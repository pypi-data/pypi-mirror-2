#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

VERSION = "0.5.5"

setup(
    name = "pylcdui",
    version = VERSION,
    description = "Library for CrystalFontz and Matrix-Orbital LCD displays",
    author = "mike wakerly",
    author_email = "opensource@hoho.com",
    url = "http://code.google.com/p/pylcdui/",
    packages = find_packages(),
    install_requires = [
      'pyserial',
    ]
)
