#! /usr/bin/env python
# encoding: utf-8

from distutils.core import setup


setup(
    name='Collectors',
    version='0.1',
    author=u'Stefan Scherfke and Ontje Luensdorf',
    author_email='stefan at sofa-rockers.org',
    description='Monitor your (SimPy) simulation models or other objects and '
        'collect data from them.',
    long_description=open('README.txt').read(),
    url='http://stefan.sofa-rockers.org/Collectors/',
    download_url='http://bitbucket.org/scherfke/collectors/downloads/',
    license='BSD',
    packages=[
        'collectors',
        'collectors.test',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
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
