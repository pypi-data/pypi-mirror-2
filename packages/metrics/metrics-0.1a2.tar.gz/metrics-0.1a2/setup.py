#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    def find_packages():
        return [
            'metrics',
        ]
    have_setuptools = False

requires = ['Pygments>=0.8']

setup(
    author = 'Mark Fink',
    author_email = 'mark@mark-fink.de',
    description = 'metrics produces metrics for C, C++, Javascript, and Python programs',
    url = 'http://bitbucket.org/markfink/metrics/',
    download_url='http://pypi.python.org/pypi/metrics',
    name='metrics',
    version='0.1a2',
    packages = find_packages(),
    license='GNU LESSER GENERAL PUBLIC LICENSE, Version 3',
    long_description=open('README').read(),
    scripts=['bin/metrics',],
    test_suite='nose.collector',
    test_requires=['nose', 'coverage'],
    platforms = 'any',
    zip_safe = False,
    include_package_data = True,
    classifiers = [
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Natural Language :: English',
    ],
)
