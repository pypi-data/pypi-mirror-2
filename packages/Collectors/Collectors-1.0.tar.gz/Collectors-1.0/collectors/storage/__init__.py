# coding=utf-8

"""
This module contains some advanced storage classes.

For your convenience, you can import the following classes directly from :mod:`collectors.storage`:

- :class:`~collectors.storage.excel.Excel`
- :class:`~collectors.storage.pytables.PyTables`

"""

try:
    from collectors.storage.excel import Excel, ExcelSeries
except ImportError:
    pass

try:
    from collectors.storage.pytables import PyTables
except ImportError as e:
    pass
