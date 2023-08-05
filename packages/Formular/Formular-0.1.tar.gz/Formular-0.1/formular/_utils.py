#!/usr/bin/env python
# coding: utf-8
"""
    formular._utils
    ~~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from inspect import getargspec
from itertools import izip

def _make_name(parent, child):
    """
    >>> _make_name(None, "eggs")
    "eggs"
    >>> _make_name("spam", "eggs")
    "spam.eggs"
    """
    if parent is None:
        return child
    return ".".join([parent, child])

def _get_args(func):
    """
    Returns the positional arguments and the keyword arguments of a given
    function.
    """
    argspec = getargspec(func)
    params = [[arg] for arg in argspec.args]
    for param, default in izip(reversed(params),
                               reversed(argspec.defaults or [])):
        param.append(default)
    args = []
    kwargs = {}
    for param in params:
        if len(param) == 1:
            args.append(param[0])
        else:
            kwargs[param[0]] = param[1]
    return args, kwargs

def _get_cls_args(cls):
    """
    Returns the positional arguments and the keyword arguments of a given
    class. 
    
    The keyword arguments will contain any keyword argument used in any
    superclass of the given class.
    """
    kwargs = set()
    for c in cls.mro()[:-1]:
        kwargs.update(_get_args(c.__init__)[1])
    args = _get_args(cls.__init__)[0]
    return args[1:], kwargs.difference(args)

def _value_matches_choice(value, choice):
    """
    Returns ``True`` if the given `value` matches the given `choice`.
    """
    # Changes made here must be made in
    # :class:`formular.fields.MultiChoiceField`, too.
    return value == choice or unicode(value) == unicode(choice)

def _is_choice_selected(field, choice):
    """
    Returns ``True`` if the given choice is one of the choices selected by the
    given `field`.
    """
    if hasattr(field.value, "__iter__"):
        return any(_value_matches_choice(v, choice) for v in field.value)
    return _value_matches_choice(field.value, choice)

def _iter_choices(choices):
    """
    Yields ``(value, label)`` tuples for the given `choices`.
    """
    for choice in choices:
        if not isinstance(choice, tuple):
            choice = (choice, choice)
        yield choice

def _to_list(obj):
    """
    Returns a list representing the given `obj` if it's iterable and not a
    string or a list containing the given `obj` otherwise.
    """
    if isinstance(obj, basestring):
        return [obj]
    try:
        return list(obj)
    except TypeError:
        return [obj]

__all__ = [
    "_make_name", "_get_args", "_get_cls_args", "_value_matches_choice",
    "_to_list"
]
