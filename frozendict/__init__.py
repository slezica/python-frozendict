import collections
import operator
import functools
import sys


try:
    from collections import OrderedDict
except ImportError:  # python < 2.7
    OrderedDict = NotImplemented


iteritems = getattr(dict, 'iteritems', dict.items) # py2-3 compatibility


class frozendict(collections.Mapping):
    """
    An immutable wrapper around dictionaries that implements the complete :py:class:`collections.Mapping`
    interface. It can be used as a drop-in replacement for dictionaries where immutability is desired.
    """

    dict_cls = dict

    def __new__(cls, *args, **kwargs):
        if args and not kwargs and type(args[0]) == cls and cls in (frozendict, FrozenOrderedDict):
            return args[0]
        return super(frozendict, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        self._dict = self.dict_cls(*args, **kwargs)
        self._hash = None

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in iteritems(self._dict):
                h ^= hash((key, value))
            self._hash = h
        return self._hash


class FrozenOrderedDict(frozendict):
    """
    A frozendict subclass that maintains key order
    """

    dict_cls = OrderedDict


if OrderedDict is NotImplemented:
    del FrozenOrderedDict
