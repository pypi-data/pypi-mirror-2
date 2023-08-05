# encoding: utf-8

from unittest import TestCase

from mock import Mock
from nose.tools import assert_raises

from collectors import core


class BaseStorageTest(TestCase):

    def test_append(self):
        assert_raises(NotImplementedError,
                core.BaseStorage().append, None, None)

    def test_create_series(self):
        assert_raises(NotImplementedError,
                core.BaseStorage().create_series, None, None)


class DefaultStorage(TestCase):

    def test_append(self):
        a_list = []
        core.DefaultStorage().append(a_list, 23)
        assert a_list == [23]

    def create_series(self):
        assert core.DefaultStorage().create_series(None, None) == []


class TestCollector(TestCase):

    def test_init(self):
        # First some fails
        assert_raises(AttributeError, core.Collector)
        assert_raises(TypeError, core.Collector, 'a', lambda: 0)
        assert_raises(ValueError, core.Collector,
                ('a', lambda: 0), ('a', lambda: 0))

        # Simple collector
        col = core.Collector(('a', lambda: 3))
        assert len(col) == 1
        assert hasattr(col, 'a')
        assert col[0] == col.a

        # With nested lists
        col = core.Collector(('a', lambda: 0),
                (('b', lambda: 0), ('c', lambda: 0)))
        assert len(col) == 3
        assert hasattr(col, 'a') and hasattr(col, 'b') and hasattr(col, 'c')

    def test_collect(self):
        a = 3
        col = core.Collector(('a', lambda: a), ('b', lambda x: x))
        col(b=1)
        assert col == ([3], [1])
        assert col.a == [3] and col.b == [1]

    def test_backends(self):
        mock = Mock()
        col = core.Collector(('a', lambda: 23), backend=mock)
        mock.create_series.assert_called_with('a', 0)

        col()
        mock.append.assert_called_with(col.a, 23)
