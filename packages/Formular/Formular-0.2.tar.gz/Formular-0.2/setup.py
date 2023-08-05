#!/usr/bin/env python
# coding: utf-8
"""
    setup
    ~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from setuptools import setup

long_description = """\
Formular is a library for validation of form-like data such as (X)HTML forms,
configurations etc.

It's designed to be simple and easy to use while being able to work with
complex nested datastructures.

If you stumble over any bugs or miss a feature feel free to create a ticket in
the `issue tracker <http://bitbucket.org/DasIch/formular/issues/>`_."""

setup(
    name="Formular",
    version="0.2",
    url="http://packages.python.org/Formular",
    license="MIT License",
    author="Daniel Neuhäuser",
    author_email="dasdasich@gmail.com",
    description="Formular is a library for validation of form-like data.",
    long_description=long_description,
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
