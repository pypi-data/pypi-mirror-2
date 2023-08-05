# encoding: utf-8
"""
Shortcut functions for :class:`~collectors.core.Collector`.
"""


def __get(obj, attr):
    """
    Helper function for :func:`get`. Returns a function which will return
    ``attr`` from ``obj`` upon calling.
    
    """
    return lambda: getattr(obj, attr)

def get(obj, *attributes):
    """
    This is a shortcut that creates lambda functions for several attributes
    of an object. All functions will automatically get the attribute’s value
    each time they are called.

    The results of ``get`` can be directly passed into a collector.

    >>> from collectors import Collector
    >>> class Spam(object):
    ...     a = 1
    ...     b = 2
    >>> spam = Spam()
    >>> get(spam, 'a', 'b') #doctest: +ELLIPSIS
    (('a', <function <lambda> at 0x...>), ('b', <function <lambda> at 0x...>))
    >>> # Create a collector with help of get:
    >>> c = Collector(get(spam, 'a', 'b'))
    >>> c() # Collect values.
    >>> c
    ([1], [2])
    
    """
    return tuple((name, __get(obj, name)) for name in attributes)

def get_objects(objs, id_attr, *attributes):
    """
    This function works similarly to :func:`get`, but it creates the lambda
    functions for multiple objects (``objs``).

    That becomes useful if you want to monitor the same attributes of several
    homogeneous objects with one :class:`~collectors.core.Collector` instance.
    The objects must have a unique attribute (``id_attr``), which will be used
    as prefix in the resulting ``(name, func)`` tuples. The value of that
    attribute should begin with a letter or an underscore.

    >>> from collectors import Collector
    >>> class Spam(object):
    ...     a = 1
    ...     b = 2
    ...     def __init__(self, obj_id):
    ...         self.obj_id = 'spam%d' % i
    ...
    >>> spams = [Spam(i) for i in range(2)]
    >>> c = Collector(get_objects(spams, 'obj_id', 'a', 'b'))
    >>> # Attributes are now named like "objid_attrname":
    >>> c.spam0_a, c.spam0_b, c.spam1_a, c.spam1_b
    ([], [], [], [])
    >>> c() # This will collect the values of a and be for each spam object.
    
    """
    buf = []
    for obj in objs:
        for attr in attributes:
            name = '%s_%s' % (str(getattr(obj, id_attr)), attr)
            buf.append((name, __get(obj, attr)))
    return tuple(buf)

def manual(value):
    """
    This a simple shortcut for a function like ``lambda x: x`` if you want to
    pass variable values manually to a monitor:

    >>> from collectors import Collector
    >>> c = Collector(('a', manual))
    >>> c(a=3)
    >>> c
    ([3],)
    
    """
    return value
