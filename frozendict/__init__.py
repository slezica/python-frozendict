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


def unfreeze(frozen):
    if type(frozen) is tuple or type(frozen) is list:
        return list(map(unfreeze, frozen))
    elif type(frozen) is OrderedDict or type(frozen) is FrozenOrderedDict:
        writable = OrderedDict()
        for key in frozen:
            writable[key] = unfreeze(frozen[key])
        return writable
    elif type(frozen) is dict or type(frozen) is frozendict:
        writable = {}
        for key in frozen:
            writable[key] = unfreeze(frozen[key])
        return writable
    else:
        return frozen


def freeze(writable):
    if type(writable) is tuple or type(writable) is list:
        return tuple(map(freeze, writable))
    elif type(writable) is OrderedDict or type(writable) is FrozenOrderedDict:
        frozen = OrderedDict()
        for key in writable:
            frozen[key] = freeze(writable[key])
        return FrozenOrderedDict(frozen)
    elif type(writable) is dict or type(writable) is frozendict:
        frozen = {}
        for key in writable:
            frozen[key] = freeze(writable[key])
        return frozendict(frozen)
    else:
        return writable
