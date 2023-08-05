#!/usr/bin/env python
# coding: utf-8
"""
    formular.datastructures
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2010 by Formular Team, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from weakref import proxy
from itertools import izip, imap
from operator import eq

class Missing(object):
    def __nonzero__(self):
        return False

    def __unicode__(self):
        return u""

    def __str__(self):
        return ""

    def __repr__(self):
        return "missing"

#: An object which is used if ``None`` cannot be used to represent a missing
#: value.
missing = Missing()

class Link(object):
    __slots__ = "next", "prev", "key", "__weakref__"

class OrderedDict(dict):
    """
    A dictionary which stores data in order of their insertion.
    """
    @classmethod
    def fromkeys(cls, iterable, default=None):
        return cls((key, default) for key in iterable)

    def __init__(self, *args, **kwargs):
        OrderedDict.clear(self)
        OrderedDict.update(self, *args, **kwargs)

    def clear(self):
        dict.clear(self)
        self._root = root = Link()
        root.prev = root.next = root
        self._map = {}

    def update(self, *args, **kwargs):
        sources = []
        if len(args) == 1:
            if hasattr(args[0], "iteritems"):
                sources.append(args[0].iteritems())
            else:
                sources.append(args[0])
        elif args:
            raise TypeError("expected at most 1 positional argument")
        if kwargs:
            sources.append(kwargs.iteritems())
        for mapping in sources:
            for key, value in mapping:
                self[key] = value

    def __setitem__(self, key, value):
        if key not in self:
            self._map[key] = link = Link()
            link.prev, link.next, link.key = self._root.prev, self._root, key
            self._root.prev.next = self._root.prev = proxy(link)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        link = self._map.pop(key)
        link.prev.next = link.next
        link.next.prev = link.prev

    def __iter__(self):
        curr = self._root.next
        while curr is not self._root:
            yield curr.key
            curr = curr.next

    def __reversed__(self):
        curr = self._root.prev
        while curr is not self._root:
            yield curr.key
            curr = curr.prev

    def iterkeys(self):
        return iter(self)

    def itervalues(self):
        return (self[key] for key in self)

    def iteritems(self):
        return izip(self.iterkeys(), self.itervalues())

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def popitem(self, last=True):
        """
        Pops the last item if `last` is ``True`` or the first item if `last` is
        ``True``.
        """
        if not self:
            raise KeyError("dictionary is empty")
        key = (reversed(self) if last else iter(self)).next()
        return key, self.pop(key)

    def pop(self, key, default=missing):
        value = self[key] if default is missing else self.get(key, missing)
        del self[key]
        return value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self) == len(other) and all(
                imap(eq, self.iteritems(), other.iteritems())
            )
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.items())

__all__ = ["missing", "OrderedDict"]
