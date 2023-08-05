#!/usr/bin/env python
# vim:ts=4:sw=4:et

from setuptools import setup

import unitstorm

setup(
    name='unitstorm',
    version=unitstorm.__version__,
    description="Unit testing microframework for Storm ORM models",
    long_description=open('README.rest').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Software Development :: Testing"
    ],
    keywords='unit test testing unittest unittesting storm orm db dbms rdbms sql fixture fixtures postgres postgresql mysql sqlite',
    author=unitstorm.__author__,
    author_email=unitstorm.__email__,
    url='http://pypi.python.org/pypi/unitstorm',
    license='LGPL 2.1',
    py_modules=["unitstorm"],
    test_suite='nose.collector',
    zip_safe=True,
    install_requires=['storm']
)
