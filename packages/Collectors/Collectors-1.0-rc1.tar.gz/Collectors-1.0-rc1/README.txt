
Collectors
==========

*Collectors* was initially developed to monitor 
`SimPy <http://simpy.sourceforge.net/>`_ simulation models but it can also be used to monitor any Python objects and collect data from them.

Our main development goals were:

* Ease of use (simple API, little typing)
* Memory and CPU efficiency

  * No impact on simulation speed if you don’t use it.
  * As little impact as possible if you use it.

* Flexibility and easy extensibility
* Separation of data collection and data analysis

Simple usage example
--------------------

    >>> class Spam(object):
    ...     a = 1
    ...     b = 2
    ...
    >>> spam = Spam()
    >>>
    >>> # Create and configure the collector
    >>> col = Collector(
    ...     ('a', lambda: spam.a),
    ...     ('b', lambda: self.b)
    ... )
    >>>
    >>> # Collect all monitored variables (spam.a and spam.b)
    >>> col()
    >>> spam.a, spam.b = 3, 4
    >>> col()
    >>>
    >>> # Get the collector’s data
    >>> col
    ([1, 3], [2, 4])
    >>> # You can also access it's elements by their name ...
    >>> col.a
    [1, 3]
    >>> # ... or by their index
    >>> col[1]
    [2, 4]


Requirements
------------

*Collectors* has only been tested with *Python 2.6* but older versions should
also work. *Python 3.0* might also work; if not, we’ll put it on our schedule.


Installation
------------

The easiest way to install *Collectors* is via *PIP* or *distribute*::

    pip install Collectors
    
or ::

    easy_install Collectors

If you downloaded the archive, execute::

    python setup.py install
    
And finally, if you checked out the repository and always want to use the newest 
version, type::

    pip install -e path/to/Collectors
    
or ::

    pip install -e https+hg://bitbucket.org/scherfke/collectors/
    

Usage
-----

The Documentation can be found in the *docs/* directory or
`online <http://stefan.sofa-rockers.org/docs/Collectors/>`_.
