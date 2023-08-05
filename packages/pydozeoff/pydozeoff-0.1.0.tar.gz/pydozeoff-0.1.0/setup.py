#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "pydozeoff",
    version = "0.1.0",
    author = "Daniel Fernandes Martins",
    author_email = 'daniel@destaquenet.com',
    url = "http://github.com/danielfm/pydozeoff",
    description = "pydozeoff is a web-based presentation engine for programmers",
    license = "BSD",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Topic :: Communications",
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    platforms = [
        "Any",
    ],

    # Dependencies
    install_requires = ["bottle>=0.6", "Jinja2>=2.3", "Pygments>=1.3"],

    # Executable scripts
    scripts = ["bin/pydozeoff"],

    # Source code structure
    packages = find_packages("src"),
    package_dir = {"": "src"},
    zip_safe = False,

    long_description = 
"""
pydozeoff is a web application written in `Python`_ that generates web-based
presentations.

As a Linux user, I don't have access to so called "professional" presentation
softwares such as Apple Keynote or MS PowerPoint. OpenOffice Impress used to be
my first choice, but I gave up using it since it's a memory/processor hog for
medium-sized presentations.

After a little research, I came across a wonderful tool called `S5`_. It was a
perfect fit, except for the one-big-fat-presentation-html thing and the lack of
syntax highlighting.

This is what I'm trying to solve with this project.

.. _Python: http://python.org/
.. _S5: http://meyerweb.com/eric/tools/s5/
""")
