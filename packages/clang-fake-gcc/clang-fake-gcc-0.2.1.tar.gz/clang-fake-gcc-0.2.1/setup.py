#!/usr/bin/env python

# You know, I always wondered why you'd force people to import stuff from your
# own package's internals, so to speak.
from distutils.core import setup

long_desc = """
clang-fake-gcc
==============

Strip out useless arguments out of gcc calls when going for clang.

This thing is especially useful for you guys who like to compile Python
extensions in C with Clang::

    CC=clang-fake-gcc python setup.py build

Nice, huh?
""".lstrip("\n")

setup(name="clang-fake-gcc", version="0.2.1",
      description=("A GCC-like compiler interface, but runs Clang instead. "
                   "Isn't that neat?"),
      author="Ludvig Ericson", author_email="ludvig@sendapatch.se",
      url="http://sendapatch.se/", long_description=long_desc,
      scripts=["clang-fake-gcc"])
