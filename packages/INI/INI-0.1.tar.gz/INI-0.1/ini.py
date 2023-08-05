#!/usr/bin/env python
# coding: utf-8
"""
    ini
    ~~~
    This module provides simple and easy loading and dumping of configuration
    files in ini format.

    :copyright: 2010 by the INI Team, see AUTHORS for details.
    :license: MIT, see LICENSE for details.
"""
from weakref import proxy
from itertools import imap
from operator import eq

__version__ = (0, 1)

#: Represents a missing value if ``None`` cannot be used.
missing = object()

class Link(object):
    __slots__ = "next", "prev", "key", "__weakref__"

class OrderedDict(dict):
    """
    A dictionary which stores items in order of their insertion.
    """
    @classmethod
    def fromkeys(cls, iterable, default=None):
        return cls((key, default) for key in iterable)

    def __init__(self, *args, **kwargs):
        # we want to support mixins which modify clear and update
        OrderedDict.clear(self)
        OrderedDict.update(self, *args, **kwargs)

    def clear(self):
        dict.clear(self)
        self._root = Link()
        self._root.prev = self._root.next = self._root
        self._map = {}

    def update(self, *args, **kwargs):
        sources = []
        if len(args) == 1:
            if hasattr(args[0], "iteritems"):
                sources.append(args[0].iteritems())
            elif hasattr(args[0], "items"):
                sources.append(args[0].items())
            else:
                sources.append(args[0])
        elif args:
            raise TypeError("expected at most one positional argument")
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
        return ((key, self[key]) for key in self)

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def setdefault(self, key, default=None):
        """
        Returns the value of the given `key` if possible otherwise `default`
        will be set as value for the given `key` and returned.
        """
        if key not in self:
            self[key] = default
        return self[key]

    def popitem(self, last=True):
        """
        Pops and returns the last item from the dict if `last` is ``True``
        otherwise the first item will be used.
        """
        if not self:
            raise KeyError("dictionary is empty")
        key = (reversed(self) if last else iter(self)).next()
        return key, self.pop(key)

    def pop(self, key, default=missing):
        if key in self:
            value = self[key]
            del self[key]
            return value
        elif default is missing:
            raise KeyError(key)
        return default

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self) == len(other) and all(
                imap(eq, self.iteritems(), other.iteritems())
            )
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{0}({1!r})".format(self.__class__.__name__, self.items())

def load(ini_file, section_seperator="."):
    """
    Parses the given `ini_file` which has to be an iterable over the lines of
    the ini formatted file or string and returns a nested :class:`OrderedDict`.
    The :class:`OrderedDict` holds the items in the order they are in the given
    `ini_file`.

    If you have nested sections this function will parse and nest them
    appropriately. Just specify the character you use with the
    `section_seperator` keyword argument.
    """
    rv = OrderedDict()
    for line in ini_file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        elif line[0] == "[" and line[-1] == "]":
            sections = line[1:-1].split(section_seperator)
            container = rv
            for section in sections:
                container = container.setdefault(section, OrderedDict())
        else:
            key, value = line.split("=")
            container[key.strip()] = value.strip()
    return rv

def _encode_flat(d, seperator):
    rv = OrderedDict()
    for key, value in d.iteritems():
        if isinstance(value, dict):
            for k, v in _encode_flat(value, seperator).iteritems():
                rv[key + seperator + k] = v
        else:
            rv[key] = value
    return rv

def dump(d, ini_file, section_seperator="."):
    """
    Dumps the arbitary deeply nested dictionary `d` to the given `ini_file`
    in ini format.
    
    Use the `section_seperator` keyword argument to specify which character
    should be used to join nested sections.
    """
    flat_d = _encode_flat(d, section_seperator)
    dumpable = OrderedDict()
    for key, value in flat_d.iteritems():
        section, key = key.rsplit(section_seperator, 1)
        dumpable.setdefault(section, OrderedDict())[key] = value
    for section, items in dumpable.iteritems():
        ini_file.write("[{0}]\n".format(section))
        for key, value in items.iteritems():
            ini_file.write("{0} = {1}\n".format(key, value))

__all__ = ["OrderedDict", "load", "dump"]
