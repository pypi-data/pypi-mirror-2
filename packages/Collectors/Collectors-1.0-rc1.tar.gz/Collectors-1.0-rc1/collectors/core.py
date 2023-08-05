# encoding: utf-8

"""
This module contains *Collector’s* core classes like like the :class:`Collector` 
itself and the base base and default storages.
"""

class BaseStorage(object):
    """
    Base class for storages.
    
    Storages define, where and in which format the collected data will be
    stored. During its initialization a :class:`Collector` will call
    :meth:`create_series` for each monitored variable. Every time the
    :class:`Collector` is asked to collect the current values :meth:`append`
    invoked with the appropiate series and value.
    
    """

    def append(self, series, value):
        """
        Append ``value`` to ``series``.
        
        You can either override this method in a subclass or assign an existing 
        method (or lambda function) to the attribute ``self.append``.
        
        """
        raise NotImplementedError(self)

    def create_series(self, name, index):
        """
        Create a new series for the variable ``name`` at ``index`` of the
        collector.
        
        """
        raise NotImplementedError(self)


class DefaultStorage(BaseStorage):
    """
    The default storage used by :class:`Collector`. The values of each
    monitored variable are stored in a simple :class:`list`.
    
    """
    def __init__(self):
        # Because the collector will always invoke append(series, value) we can
        # use the list.append function directly.
        self.append = list.append

    def create_series(self, name, index):
        """Return a new empty list."""
        return []


class Collector(tuple):
    """
    This class can monitor the values of a given set of variables.

    Each variable is described by a *name* and a *collector function* which must
    be passed as tuple ``(name, func)``. The list of *name*-*func*-tuples may
    also be nested, which is helpful for some convenience functions.
    
    For each variable a *series* for the observed values will be created. The
    variables’ *series* are accessible via an index (defined by the order you
    passed them) as well as by an attribute of a ``Collector`` instance named
    after *name*.

    All collector functions will be called (in the same order as they were
    specified) each time a ``Collector`` instance is called. The collector
    functions may either grab the desired values by themselves or let them be
    passed manually with each collector call.

    Here is an example how this works:

    >>> class Spam(object):
    ...     a = 1
    ...     b = 2
    ...
    >>> spam = Spam()
    >>> c = Collector(('a', lambda: spam.a), ('b', lambda x: x))
    >>> c.a == c[0], c.b == c[1]
    (True, True)
    >>>
    >>> c(b=spam.b + 2)
    >>> spam.a, spam.b = 3, 4
    >>> c(b=spam.b + 2)
    >>> c # Collector inherits tuple, so you can do this:
    ([1, 3], [4, 6])
    >>> c.a, c.b # You can also access it's elements by their name.
    ([1, 3], [4, 6])

    In this example, ``spam`` is the object to be monitored. The monitor is
    configured to observe two variables named “a” and “b”. The collector
    function for “a” automatically retrieves ``spam.a``, while the value for “b”
    needs to be passed to the monitor manually as a keyword argument. For these
    common cases, there are the shortcuts :func:`~collectors.shortcuts.get` and
    :func:`~collectors.shortcuts.manual`.

    Note that names for data series need to be unique. ``Collector``
    instanciation will raise a ``ValueError`` if there's a duplicate name.

    """
    def __new__(cls, *args, **kwargs):
        # We need to override __new__ instead of __init__ because tuples are
        # immutable. This means it's data is set during the allocation phase in
        # __new__.
        if not args:
            raise AttributeError('Nothing to be monitored.')

        backend = kwargs['backend'] \
                if 'backend' in kwargs else DefaultStorage()

        # Parse arguments using a helper function. This method will populate the
        # following lists.
        names, collectors, series = [], [], []

        def parse_arg(arg):
            """
            Method for parsing collector descriptions.

            ``arg`` can be ('name', func) or (('name1', func),
            ('name2', func), ...)
            
            """
            if type(arg) != tuple:
                raise TypeError('%s must be an instance of '
                        '"collections.Iterable", but %s is not.' %
                        (arg, type(arg)))

            # Check if this is a collector description. These look like this:
            # ('name', func). Otherwise treat arg as a nested list of collector
            # descriptions.
            if len(arg) == 2 and isinstance(arg[0], basestring) and \
                    callable(arg[1]):
                if arg[0] in names:
                    raise ValueError(
                            'There\'s already a series named "%s".' % arg[0])
                names.append(arg[0])
                collectors.append(arg[1])
                series.append(backend.create_series(arg[0], len(series)))
            else:
                # This is a nested list of collector descriptions. Recurse.
                for child in arg:
                    parse_arg(child)

        # Parse all arguments.
        for arg in args:
            parse_arg(arg)

        # Allocate the tuple instance and set the empty series lists as data.
        instance = tuple.__new__(cls, series)

        # Set the names and collectors of each series.
        instance.__append = backend.append
        instance.__names = tuple(names)
        instance.__collectors = tuple(collectors)

        # Link attributes to series.
        for name, data in zip(names, series):
            setattr(instance, name, data)

        return instance

    def __call__(self, **kwargs):
        """
        Execute all collector functions and append the retrieved values to the
        series of each variable.
        
        If a collector function required a parameter, you must pass it as
        keyword argument with the variable’s name.
        
        """
        for series, name, col in zip(self, self.__names, self.__collectors):
            if name in kwargs:
                self.__append(series, col(kwargs[name]))
            else:
                self.__append(series, col())

    collect = __call__
    """This is just an alias to :meth:`__call__`."""
