#!/usr/bin/env python
# coding: utf-8
"""
    formular.validators
    ~~~~~~~~~~~~~~~~~~~

    Provides the builtin validators.
    
    A validator is just a function which takes the form, an initial value and
    the value we got from the user/client, and returns ``False`` if it failed
    or ``True`` otherwise.

    Validators do not raise exceptions because the message we want to display
    might depend on the field, e.g. a text field wants to display a different
    message then a multiple field although both use the min_length and 
    max_length validators.

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from functools import wraps
import re

def as_validator(func):
    """
    Given a function like::

        def required(form, is_required, value):
            return bool(value) if is_required else True

    :func:`as_validator` returns a factory function::

        >>> required_factory(required)
        >>> required_factory(True)(form, u"")
        False
        >>> required_factory(False)(form, u"")

    If you do not care about the original function you can use
    :func:`as_validator` to decorate the function.
    """
    @wraps(func)
    def validator_factory(initial_value):
        def validator(form, value):
            # Some error messages require information about the validator,
            # and information why it failed. So we have to expose some
            # information.
            # This is used in
            # :meth:`formular.fields.Field._format_error_message`.
            validator.last_args = {
                "form": form,
                "initial_value": initial_value,
                "value": value
            }
            return func(form, initial_value, value)
        validator.initial_value = initial_value
        return validator
    return validator_factory

@as_validator
def required(form, is_required, value):
    """
    Checks if the boolean value of `value` is ``True`` if `is_required` is
    ``True``.
    """
    return bool(value) if is_required else True

@as_validator
def requires(form, field_name, value):
    """
    Checks if the field with the given name has a value if the validated field
    has a value.
    """
    return bool(form.fields[field_name].value) if value else True

@as_validator
def equals(form, field_name, value):
    """
    Checks if the value of the field with the given name has the same value
    as the validated field.
    """
    return form.fields[field_name].value == value

@as_validator
def min_length(form, min_length, value):
    return len(value) > min_length

@as_validator
def max_length(form, max_length, value):
    return len(value) < max_length

@as_validator
def min_value(form, min_value, value):
    return value > min_value

@as_validator
def max_value(form, max_value, value):
    return value < max_value

_username_re = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
_domain_re = re.compile(r"""
        ^(?:[a-z0-9][a-z0-9\-]{0,62}\.)+ # (sub)domain
        [a-z]{2,}$ # top-level domain
        """,
        re.I | re.VERBOSE
)
@as_validator
def is_email(form, initial_value, value):
    if not value.count(u"@") == 1:
        return not initial_value
    local, domain = value.split(u"@")
    if not _username_re.search(local):
        return not initial_value
    if not _domain_re.search(domain):
        return not initial_value
    return initial_value

__all__ = [
    "as_validator", "required", "requires", "equals", "min_length",
    "max_length", "min_value", "max_value", "is_email"
]
