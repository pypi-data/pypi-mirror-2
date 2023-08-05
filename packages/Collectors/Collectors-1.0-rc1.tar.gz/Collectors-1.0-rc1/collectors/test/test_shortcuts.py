# encoding: utf-8

from collectors import shortcuts


class Spam(object):
    a = 1
    b = 2

    def __init__(self, i):
        self.i = i


def test___get():
    spam = Spam(0)

    func = shortcuts.__get(spam, 'a')

    assert func() == spam.a

def test_get():
    spam = Spam(0)

    attrs = ('a', 'b')
    tuples = shortcuts.get(spam, *attrs)

    assert len(tuples) == len(attrs)

    for attr, (name, func) in zip(attrs, tuples):
        assert attr == name
        assert func() == getattr(spam, attr)

def test_get_objects():
    spams = [Spam(i) for i in range(3)]

    attrs = ('a', 'b')
    tuples = shortcuts.get_objects(spams, 'i', *attrs)

    assert len(tuples) == len(spams) * len(attrs)

    i = 0
    for spam in spams:
        for attr in attrs:
            assert tuples[i][0] == str(spam.i) + '_' + attr
            assert tuples[i][1]() == getattr(spam, attr)

            i += 1

def test_manual():
    assert shortcuts.manual(23) == 23
