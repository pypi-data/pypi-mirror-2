# encoding: utf-8

from unittest import TestCase

from nose.tools import assert_raises
import xlwt

from collectors.storage.excel import Excel, ExcelSeries


class ExcelTest(TestCase):

    def setUp(self):
        self.w = xlwt.Workbook()
        self.excel = Excel(self.w, 'foo')

    def test_init(self):
        s = self.w.add_sheet('bar')
        excel = Excel(self.w, s)
        assert self.w.get_sheet(0).get_name() == 'foo'
        assert self.w.get_sheet(1).get_name() == 'bar'
        assert self.w.get_sheet(1) == s
        assert_raises(IndexError, self.w.get_sheet, 2)

    def test_create_series(self):
        series = self.excel.create_series('bar', 0)

        assert isinstance(series, ExcelSeries)
        assert series.sheet == self.excel.sheet
        assert series.col_name == 'bar'
        assert series.col_index == 0

    def test_append(self):
        series = self.excel.create_series('bar', 0)
        assert len(self.excel.sheet.rows) == 1, self.excel.sheet.rows
        self.excel.append(series, 3)
        assert len(self.excel.sheet.rows) == 2
