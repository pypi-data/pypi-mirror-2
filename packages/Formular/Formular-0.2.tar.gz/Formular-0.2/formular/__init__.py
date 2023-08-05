#!/usr/bin/env python
# coding: utf-8
"""
    formular
    ~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import formular.fields
import formular.forms
import formular.widgets

__version__ = (0, 2)

def setup():
    import sys

    from formular.extensions import load
    extensions = load()
    module_attributes = {
        "fields": {},
        "forms": {},
        "widgets": {}
    }

    for extension in extensions:
        for key, value in extension.iteritems():
            module_attributes[key].update(value)

    for module_name, attributes in module_attributes.iteritems():
        module = sys.modules["formular." + module_name]
        for name, attribute in attributes.iteritems():
            setattr(module, name, attribute)

setup()
del setup
