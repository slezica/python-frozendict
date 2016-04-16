from unittest import TestCase

from frozendict import frozendict, FrozenOrderedDict


class MyTestCase(TestCase):
    def assertMappingEqual(self, m1, m2):
        # This will not do as strict type compatibility check between m1 and m2 as
        # self.assertEqual or self.assertDictEqual and set assertions give very
        # easy to read error messages in unittest.
        self.assertSetEqual(set(m1.items()), set(m2.items()))


def _assign_to_dict(dict_instance, key, value):
    dict_instance[key] = value


class TestFrozenDict(MyTestCase):
    def test_assignment_fails(self):
        self.assertRaisesRegexp(
            TypeError,
            r'object does not support item assignment',
            _assign_to_dict,
            frozendict(),
            'key',
            'value',
        )

    def test_init(self):
        frozendict()

    def test_init_with_keys(self):
        frozen = frozendict(a=0, b=1)
        self.assertMappingEqual(frozen, dict(a=0, b=1))

    def test_init_with_dict(self):
        frozen = frozendict(dict(a=0, b=1))
        self.assertMappingEqual(frozen, dict(a=0, b=1))

    def test_init_with_dict_and_keys(self):
        frozen = frozendict(dict(a=0, b=1), b=2, c=3)
        self.assertMappingEqual(frozen, dict(a=0, b=2, c=3))

    def test_getitem(self):
        frozen = frozendict(key='value')
        self.assertEqual(frozen['key'], 'value')

    def test_copy(self):
        frozen = frozendict(a=0, b=1)
        copied = frozen.copy()
        self.assertIs(type(copied), type(frozen))
        self.assertMappingEqual(copied, frozen)

    def test_copy_with_keys(self):
        frozen = frozendict(a=0, b=1)
        copied = frozen.copy(b=2, c=3)
        self.assertIs(type(copied), type(frozen))
        self.assertMappingEqual(copied, dict(a=0, b=2, c=3))

    def test_iter(self):
        frozen = frozendict(a=0, b=1)
        keys = {key for key in frozen}
        self.assertSetEqual(keys, {'a', 'b'})

    def test_len(self):
        frozen = frozendict(a=0, b=1)
        self.assertEqual(len(frozen), 2)

    def test_repr(self):
        frozen = frozendict(a=0, b=1)
        r = repr(frozen)
        self.assertTrue(r.startswith('<frozendict '))
        self.assertTrue(r.endswith('>'))

    def test_hash(self):
        frozen = frozendict(a=0, b=1)
        hash(frozen)


class TestFrozenOrderedDict(MyTestCase):
    def test_assignment_fails(self):
        self.assertRaisesRegexp(
            TypeError,
            r'object does not support item assignment',
            _assign_to_dict,
            FrozenOrderedDict(),
            'key',
            'value',
        )

    def test_init(self):
        FrozenOrderedDict()

    def test_init_with_keys(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        self.assertMappingEqual(frozen, dict(a=0, b=1))

    def test_init_with_dict(self):
        frozen = FrozenOrderedDict(dict(a=0, b=1))
        self.assertMappingEqual(frozen, dict(a=0, b=1))

    def test_init_with_dict_and_keys(self):
        frozen = FrozenOrderedDict(dict(a=0, b=1), b=2, c=3)
        self.assertMappingEqual(frozen, dict(a=0, b=2, c=3))

    def test_getitem(self):
        frozen = FrozenOrderedDict(key='value')
        self.assertEqual(frozen['key'], 'value')

    def test_copy(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        copied = frozen.copy()
        self.assertIs(type(copied), type(frozen))
        self.assertMappingEqual(copied, frozen)

    def test_copy_with_keys(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        copied = frozen.copy(b=2, c=3)
        self.assertIs(type(copied), type(frozen))
        self.assertMappingEqual(copied, dict(a=0, b=2, c=3))

    def test_iter(self):
        frozen = FrozenOrderedDict([('a', 0), ('c', 2), ('b', 1), ('d', 3)])
        keys = [key for key in frozen]
        # order should be kept
        self.assertListEqual(keys, ['a', 'c', 'b', 'd'])

    def test_len(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        self.assertEqual(len(frozen), 2)

    def test_repr(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        r = repr(frozen)
        self.assertTrue(r.startswith('<FrozenOrderedDict '))
        self.assertTrue(r.endswith('>'))

    def test_hash(self):
        frozen = FrozenOrderedDict(a=0, b=1)
        hash(frozen)
