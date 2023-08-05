#!/usr/bin/env python
# coding: utf-8
"""
    setup
    ~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup

setup(
    name="Formular",
    version="0.1",
    url="http://packages.python.org/Formular",
    license="MIT License",
    author="Daniel Neuhäuser",
    author_email="dasdasich@gmail.com",
    description="Formular is a library for validation of form-like data.",
    keywords="forms",
    packages=[
        "formular",
        "formular.i18n"
    ],
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Topic :: Internet :: WWW/HTTP"
    ]
)
