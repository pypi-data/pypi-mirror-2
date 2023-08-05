# encoding: utf-8

"""
.. module:: monitoring
   :platform: Mac, Unix, Windows
   :synopsis: Monitor SimPy simulations.
.. moduleauthor:: Ontje Lünsdorf
.. moduleauthor:: Stefan Scherfke

This module contains the proposal for a new approach for monitoring SimPy
simulations.
"""


class Monitor(tuple):
    """This class can monitor the values of a given set of variables.

    Each variable is described by a *name* and a *collector function*. The
    list of all variable values is accessible as attribute of a monitor
    instance as well as via an index (defined by the order you passed them to
    ``__init__``). Besides *(name, func)* tuples you can also pass nested
    lists of those tuples, which is helpful for some convenience functions.

    All collectors will be called (in the same order as they were specified)
    each time a ``Monitor`` instance is called. The collector functions may
    either grab the desired values by themselves or let them be passed
    manually with each monitor call.

    Here is an example how this works:

    >>> class Spam(object):
    ...     a = 1
    ...     b = 2
    ...
    >>> spam = Spam()
    >>> m = Monitor(('a', lambda: getattr(spam, 'a')), ('b', lambda x: x))
    >>> m.a == m[0], m.b == m[1]
    (True, True)
    >>>
    >>> m(b=spam.b + 2)
    >>> m # Monitor is a tuple with nested lists by itself.
    ([1], [4])
    >>> m.a, m.b # You can also access it's elements by their name.
    ([1], [4])

    In this example, ``spam`` is the object to be monitored. The monitor is
    configured to observe two variables named “a” and “b”. The collector for
    “a” automatically retrieves it’s value via ``getattr()`` while the value
    for “b” needs to be passed to the monitor manually as keyword argument.
    For these common cases, there are the shortcuts :func:`get` and
    :func:`manual`.

    Note that names for data series need to be unique. ``Monitor``
    instanciation will raise a ``ValueError`` if there's a duplicate name.
    """
    def __new__(cls, *args):
        # We need to override __new__ instead of __init__ because tuples are
        # immutable. This means it's data is set during the allocation phase in
        # __new__.
        if not args:
            raise AttributeError('Nothing to be monitored.')

        # Parse arguments using a helper function. This method will populate the
        # following lists.
        names, collectors, series = [], [], []

        def parse_arg(arg):
            """Method for parsing collector descriptions.

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
                series.append([])
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
        instance.__names = tuple(names)
        instance.__collectors = tuple(collectors)

        # Link attributes to series.
        for name, data in zip(names, series):
            setattr(instance, name, data)

        return instance

    def __call__(self, **kwargs):
        for series, name, col in zip(self, self.__names, self.__collectors):
            if name in kwargs:
                series.append(col(kwargs[name]))
            else:
                series.append(col())


def __get(obj, attr):
    """Helper function for :func:`get`. Returns a function which will return
    ``attr`` of ``obj`` upon calling.
    """
    return lambda: getattr(obj, attr)

def get(obj, *attributes):
    """This is a shortcut that creates lambda functions for several attributes
    of an object. All functions will automatically get the attribute’s value
    each time they are called.

    The results of get can be directly passed into a monitor.

    >>> from collections import namedtuple
    >>> spam = namedtuple('Spam', ['a', 'b'])(1, 2)
    >>> get(spam, 'a', 'b')
    (('a', lambda: getattr(obj, attr)), ('b', lambda: getattr(obj, attr)))
    >>>
    >>> m = Monitor(get(spam, 'a', 'b'))
    >>> m() # Collect values.
    >>> m
    ([1], [2])
    """
    return tuple((name, __get(obj, name)) for name in attributes)


def manual(value):
    """This a simple shortcut for a function like ``lambda x: x`` if you want
    to pass variable values manually to a monitor:

    >>> m = Monitor(('a', manual))
    >>> m(a=3)
    >>> m
    ([3],)
    """
    return value


if __name__ == '__main__':
    import random

    import matplotlib.pyplot as plt
    from numpy import array, float64
    from SimPy.Simulation import Simulation, Process, hold


    class MyProc(Process):
        """A simple example process that illustrates the usage of the new
        monitoring approach."""
        def __init__(self, sim):
            Process.__init__(self, sim=sim)

            self.a = 0
            self.b = 0
            self.c = 0

            # Create a monitor that will collect:
            # time:     A list with timestampes from sim.now()
            # a:        Values of proc.a
            # b:        Values of proc.b
            # diff:     A value passed manually
            # square:   Square of self.c
            self.monitor = Monitor(
                ('time', sim.now),
                get(self, 'a', 'b'),
                ('diff', manual),
                ('square', lambda: self.c ** 2)
            )

        def run(self):
            while True:
                self.a += random.random()
                self.b += random.randint(1, 2)
                self.c += random.randint(2, 4)

                self.monitor(diff=self.c-self.b)

                yield hold, self, 2


    # Run the simulation
    sim = Simulation()
    proc = MyProc(sim)
    sim.activate(proc, proc.run())
    sim.simulate(until=10)

    # Just a test and a simple example how to acces the monitored values:
    assert proc.monitor[1] == proc.monitor.a

    print proc.monitor
    print zip(*proc.monitor)

    # NumPy helps you with the statistics and other calculations.
    # Note: specification of dtype gives you a massive speed-up!
    a = array(proc.monitor.a, dtype=float64)
    print 'a:', a
    # NumPy: average, std. deviation, variance
    print 'a stats:', a.mean(), a.std(), a.var()

    # This one creates a multi-dimensional array (see the output)
    np_mon = array(proc.monitor, dtype=float64)
    print 't, a, b, diff, square:\n', np_mon
    # Get the average of all monitored proc.b
    print 'b stats:', np_mon[2].mean()
    # Get the std. deviation of all monitored proc.c
    print 'c stats:', np_mon[3].std()

    # Matplotlib plots your data:
    # Either directly from a monitor ...
    plt.plot(proc.monitor.time, proc.monitor.a, 'b')
    # ... or the NumPy array
    plt.plot(np_mon[0], np_mon[2], 'r')
    plt.show()
