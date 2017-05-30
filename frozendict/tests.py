from unittest import TestCase
from collections import OrderedDict

from frozendict import frozendict, FrozenOrderedDict, freeze, unfreeze


class BaseTestCase(TestCase):
    def assertMappingEqual(self, m1, m2):
        # `assertDictEqual` will make a failing type check when comparing a `dict`
        # with a `frozendict`. Instead, we'll compare the item sets:
        self.assertSetEqual(set(m1.items()), set(m2.items()))

    def assertRaisesAssignmentError(self, *args, **kwargs):
        self.assertRaisesRegexp(
            TypeError,
            r'object does not support item assignment',
            *args, **kwargs
        )


def setitem(dct, key, value):
    dct[key] = value


class TestFrozenDict(BaseTestCase):
    def test_assignment_fails(self):
        self.assertRaisesAssignmentError(setitem, frozendict(), 'key', 'value')

    def test_init(self):
        frozendict()

    def test_init_with_keys(self):
        fd = frozendict(a=0, b=1)
        self.assertMappingEqual(fd, dict(a=0, b=1))

    def test_init_with_dict(self):
        fd = frozendict(dict(a=0, b=1))
        self.assertMappingEqual(fd, dict(a=0, b=1))

    def test_init_with_dict_and_keys(self):
        fd = frozendict(dict(a=0, b=1), b=2, c=3)
        self.assertMappingEqual(fd, dict(a=0, b=2, c=3))

    def test_getitem(self):
        fd = frozendict(key='value')
        self.assertEqual(fd['key'], 'value')

    def test_copy(self):
        fd = frozendict(a=0, b=1)
        copied = fd.copy()
        self.assertIs(type(copied), type(fd))
        self.assertMappingEqual(copied, fd)

    def test_copy_with_keys(self):
        fd = frozendict(a=0, b=1)
        copied = fd.copy(b=2, c=3)
        self.assertIs(type(copied), type(fd))
        self.assertMappingEqual(copied, dict(a=0, b=2, c=3))

    def test_iter(self):
        fd = frozendict(a=0, b=1)
        keys = {key for key in fd}
        self.assertSetEqual(keys, {'a', 'b'})

    def test_len(self):
        fd = frozendict(a=0, b=1)
        self.assertEqual(len(fd), 2)

    def test_repr(self):
        fd = frozendict(a=0, b=1)
        r = repr(fd)
        self.assertTrue(r.startswith('<frozendict '))
        self.assertTrue(r.endswith('>'))

    def test_hash(self):
        fd = frozendict(a=0, b=1)
        hash(fd)


class TestFrozenOrderedDict(BaseTestCase):
    def test_assignment_fails(self):
        self.assertRaisesAssignmentError(setitem, FrozenOrderedDict(), 'key', 'value')

    def test_init(self):
        FrozenOrderedDict()

    def test_init_with_keys(self):
        fd = FrozenOrderedDict(a=0, b=1)
        self.assertMappingEqual(fd, dict(a=0, b=1))

    def test_init_with_dict(self):
        fd = FrozenOrderedDict(dict(a=0, b=1))
        self.assertMappingEqual(fd, dict(a=0, b=1))

    def test_init_with_dict_and_keys(self):
        fd = FrozenOrderedDict(dict(a=0, b=1), b=2, c=3)
        self.assertMappingEqual(fd, dict(a=0, b=2, c=3))

    def test_getitem(self):
        fd = FrozenOrderedDict(key='value')
        self.assertEqual(fd['key'], 'value')

    def test_copy(self):
        fd = FrozenOrderedDict(a=0, b=1)
        copied = fd.copy()
        self.assertIs(type(copied), type(fd))
        self.assertMappingEqual(copied, fd)

    def test_copy_with_keys(self):
        fd = FrozenOrderedDict(a=0, b=1)
        copied = fd.copy(b=2, c=3)
        self.assertIs(type(copied), type(fd))
        self.assertMappingEqual(copied, dict(a=0, b=2, c=3))

    def test_iter(self):
        fd = FrozenOrderedDict([('a', 0), ('c', 2), ('b', 1), ('d', 3)])
        keys = [key for key in fd]
        self.assertListEqual(keys, ['a', 'c', 'b', 'd']) # verifies order

    def test_len(self):
        fd = FrozenOrderedDict(a=0, b=1)
        self.assertEqual(len(fd), 2)

    def test_repr(self):
        fd = FrozenOrderedDict(a=0, b=1)
        r = repr(fd)
        self.assertTrue(r.startswith('<FrozenOrderedDict '))
        self.assertTrue(r.endswith('>'))

    def test_hash(self):
        fd = FrozenOrderedDict(a=0, b=1)
        hash(fd)

class TestFreezeAndUnfreeze(BaseTestCase):
    def test_freeze_dict(self):
        writable = {}
        expected = frozendict(writable)
        result = freeze(writable)
        self.assertIs(type(result), type(expected))
        self.assertEqual(freeze(writable), expected)
    def test_freeze_dict2(self):
        writable = {'a': 1}
        expected = frozendict(writable)
        result = freeze(writable)
        self.assertIs(type(result), type(expected))
        self.assertEqual(freeze(writable), expected)
    def test_freeze_ordered(self):
        writable = OrderedDict({})
        expected = FrozenOrderedDict({})
        result = freeze(writable)
        self.assertIs(type(result), type(expected))
        self.assertEqual(freeze(writable), expected)
    def test_freeze_ordered2(self):
        writable = OrderedDict({'a':1})
        expected = FrozenOrderedDict({'a': 1})
        result = freeze(writable)
        self.assertIs(type(result), type(expected))
        self.assertEqual(result, expected)
    def test_freeze_list(self):
        self.assertEqual(freeze([1,2,3]), (1,2,3))
    def test_freeze_recursion(self):
        writable = {
            'a': [1,2,{'a': 1}],
            'b': 'foo',
            'c': {
                'd': {}
            },
            'e': {'f': OrderedDict({'a':1})}
        }
        expected = frozendict({
            'a': (1,2, frozendict(({'a': 1}))),
            'b': 'foo',
            'c': frozendict({
                'd': frozendict({})
            }),
            'e': {'f': FrozenOrderedDict({'a':1})}
        })
        frozen = freeze(writable)
        def modify(d, k):
            d[k] = None
        for k in expected:
            self.assertRaises(TypeError, modify, expected, k)
        for k in frozen:
            self.assertRaises(TypeError, modify, frozen, k)
        self.assertEqual(frozen, expected)
        self.assertDictEqual(unfreeze(expected), writable)
        ordered = unfreeze(expected)['e']['f']
        self.assertIs(type(ordered), OrderedDict)
        self.assertDictEqual(unfreeze(frozen), writable)
        self.assertEqual(freeze(expected), expected)

