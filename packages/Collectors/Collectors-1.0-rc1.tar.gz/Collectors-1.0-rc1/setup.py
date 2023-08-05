#! /usr/bin/env python
# encoding: utf-8

from distutils.core import setup


class UltraMagicString(object):
    # Catch-22:
    # - if I return Unicode, python setup.py --long-description as well
    #   as python setup.py upload fail with a UnicodeEncodeError
    # - if I return UTF-8 string, python setup.py sdist register
    #   fails with an UnicodeDecodeError

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode('UTF-8')

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)


setup(
    name='Collectors',
    version='1.0-rc1',
    author=UltraMagicString('Stefan Scherfke and Ontje Lünsdorf'),
    author_email='stefan at sofa-rockers.org',
    description='Monitor your (SimPy) simulation models or other objects and '
        'collect data from them.',
    long_description=UltraMagicString(open('README.txt').read()),
    url='http://stefan.sofa-rockers.org/Collectors/',
    download_url='http://bitbucket.org/scherfke/collectors/downloads/',
    license='BSD',
    packages=[
        'collectors',
        'collectors.storage',
        'collectors.test',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
