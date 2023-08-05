# encoding: utf-8

"""
If your colleagues use *MS Excel* and require your data in that format, you
want to use this storage backend. ;-)

"""

import xlwt

from collectors.core import BaseStorage


class ExcelSeries(object):
    """
    An instance of this class will be create for each series. It provides the
    ``append()`` function for :class:`Excel`.
    
    It manages a column named ``col_name`` at index ``col_index`` with in an
    excel ``sheet``. You don’t need to use this class directly. 
    
    """
    def __init__(self, sheet, col_name, col_index):
        self.sheet = sheet
        self.col_name = col_name
        self.col_index = col_index

        # Write the header.
        self.sheet.write(0, col_index, col_name)
        self.row_index = 1

    def append(self, value):
        """Append ``value`` to this series/sheet column."""
        self.sheet.write(self.row_index, self.col_index, value)
        self.row_index += 1


class Excel(BaseStorage):
    """
    Stores the collectors data in the *Excel* file/workbook ``book`` within 
    the sheet named ``sheet`` (``sheet`` may also be an existing ``Worksheet``).
    
    Example::
    
        import xlwt
        from collectors import Collector, get, storage
        class Spam(object):
            a = 1
        spam = Spam()
        book = xlwt.Workbook('my_data.xls')
        collector = Collector(get(spam, 'a'),
                backend=storage.Excel(book, 'my_sheet'))
    
    """
        
    def __init__(self, book, sheet):
        self.book = book
        self.sheet = sheet if isinstance(sheet, xlwt.Worksheet) \
                else book.add_sheet(sheet)
        
        self.append = lambda series, value: series.append(value)

    def create_series(self, name, index):
        """
        Create a new :class:`ExcelSeries` in the current sheed with the
        specified ``name`` at the position ``index``.
        """
        return ExcelSeries(self.sheet, name, index)
