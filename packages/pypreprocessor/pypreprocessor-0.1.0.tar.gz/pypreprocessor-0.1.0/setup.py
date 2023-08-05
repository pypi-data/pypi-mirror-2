#!/usr/bin/env python
# pypreprocessor's setup.py

from distutils.core import setup
setup(
    name = "pypreprocessor",
    py_modules = ['pypreprocessor'],
    version = "0.1.0",
    description = "Python Preprocessor - to run c-style preprocessor directives in python modules",
    author = "Evan Plaice",
    author_email = "evanplaice@gmail.com",
    url = "http://code.google.com/p/pypreprocessor/",
    license = "MIT",
    keywords = ["python", "preprocessor", "meta"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        ],
    long_description = open('README.txt').read()
)
