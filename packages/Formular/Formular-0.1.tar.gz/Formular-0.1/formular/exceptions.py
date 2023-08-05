#!/usr/bin/env python
# coding: utf-8
"""
    formular.exceptions
    ~~~~~~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from formular._utils import _make_name
from formular.datastructures import OrderedDict

class ValidationError(ValueError):
    """
    Represents none, one or more errors which occured during validation of a
    :class:`formular.fields.Field` instance.
    """
    def unpack(self, parent=None):
        """
        Returns the errors as a dictionary.
        """
        return {parent: self.args}

    def __nonzero__(self):
        return bool(self.args)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.unpack() == other.unpack()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

class MultipleValidationErrors(ValidationError):
    """
    Represents none, one or more errors which occured during validation of a
    :class:`formular.fields.Field` instance and it's children.
    """
    def __init__(self, errors=None):
        ValidationError.__init__(self)
        self.errors = errors or OrderedDict()

    def unpack(self, parent=None):
        """
        Returns the errors as a flat dictionary.
        """
        result = OrderedDict()
        for child, error in self.errors.iteritems():
            result.update(error.unpack(_make_name(parent, child)))
        return result

    def __nonzero__(self):
        return bool(self.errors)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.errors)

__all__ = ["ValidationError", "MultipleValidationErrors"]
