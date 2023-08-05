# encoding: utf-8

"""
`PyTables <http://pytables.org/>`_ can efficiently and easily cope with very
large amounts of data. If you are planing to collect data from e.g. very long
running simulations, you should consider using the :class:`Pytables` storage
instead of the default one to save memory.

"""

import tables

from collectors.core import BaseStorage


class PyTables(BaseStorage):
    """
    This storage stores a collector’s series as an array in a *HDF5* file. The
    series of a collector instance will be grouped together, so they can be
    addressed like ``/group_name/variable_name`` in the *HDF5* file hierarchy.
    
    :param h5file: An opend *HDF5* as returned by :func:`tables.openFile`
    :param group: A name for the group or an existing group instance
    :param dtypes: A list of data types for the series ordered in the same way
                   as the *name-func*-tuples.
    
    *PyTables* is very tightly coupled with *NumPy* and requires you to specify
    the data type for each series. You can use *NumPy’s* `type names
    <http://docs.scipy.org/doc/numpy/reference/arrays.scalars.html
    #built-in-scalar-types>`_ for that. If you call the ``read()`` for a series,
    you’ll get a *NumPy* array containing all values for that series.
    
    .. note::
        
        This backend does NO automatic flushes. *PyTables* does that only when
        you close the *HDF5* file, but you can call ``my_h5file.flush()``
        anytime you want.
                   
    Example::
    
        import tables
        from collectors import Collector, get, storage
        class Spam(object):
            a = 1
            b = 2.0
        spam = Spam()
        h5file = tables.openFile('spam.h5', mode='w')
        collector = Collector(get(spam, 'a', 'b'),
                backend=storage.PyTables(h5file, 'spam_group', ('int', 'float'))
        )
    
    """
    def __init__(self, h5file, group, dtypes):
        self.h5file = h5file
        self.group = group \
                if isinstance(group, tables.Group) \
                else self.h5file.createGroup('/', group)
        self.dtypes = dtypes
        
        self.append = lambda series, value: series.append([value])

    def create_series(self, name, index):
        """
        Create a new ``EArray`` in the collector’s group named ``named`` with
        the type that can be found at ``index`` in the data types list passed to
        ``__init__``.
        
        """
        return self.h5file.createEArray(self.group, name,
                tables.Atom.from_sctype(self.dtypes[index]), (0,))
