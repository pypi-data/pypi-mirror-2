#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "pydozeoff",
    version = "0.1.1",
    author = "Daniel Fernandes Martins",
    author_email = 'daniel@destaquenet.com',
    url = "http://github.com/danielfm/pydozeoff",
    description = "Web-based presentation engine for programmers",
    license = "BSD",
    keywords = "web presentation slideshow talk engine python s5",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
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
    entry_points = {
        'console_scripts': [
            "pydozeoff = pydozeoff:main"
        ],
    },

    # Source code structure
    packages = find_packages("src"),
    package_dir = {"": "src"},
    include_package_data = True,
    zip_safe = False,

    long_description = 
"""
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
