# encoding: utf-8

from unittest import TestCase
import tempfile

import tables

from collectors.storage.pytables import PyTables


class PyTablesTest(TestCase):

    def setUp(self):
        tmpfile = tempfile.NamedTemporaryFile(mode='r')
        h5file = tables.openFile(tmpfile.name, mode='w')

        self.pt = PyTables(h5file, 'foo', ('int', 'float'))

    def tearDown(self):
        self.pt.h5file.close()

    def test_init(self):
        assert self.pt.dtypes == ('int', 'float')
        assert self.pt.h5file.getNode('/', 'foo')

        grp = self.pt.h5file.createGroup('/', 'bar')
        pt = PyTables(self.pt.h5file, grp, ())

        assert len(pt.h5file.listNodes('/')) == 2

    def test_create_series(self):
        series = self.pt.create_series('bar', 0)
        assert series == self.pt.h5file.getNode('/foo', 'bar')

    def test_append(self):
        series = self.pt.create_series('bar', 0)
        self.pt.append(series, 23)
        assert series[0] == 23
