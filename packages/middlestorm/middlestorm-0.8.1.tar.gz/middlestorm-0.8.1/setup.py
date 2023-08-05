#!/usr/bin/env python
#
# $Id: setup.py,v 74e3e6109a58 2010/04/19 09:30:45 vsevolod $

from setuptools import setup

import middlestorm

setup(
    name='middlestorm',
    version=middlestorm.__version__,
    description="Middleware for use Storm ORM in WSGI applications",
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
    ], 
    keywords='wsgi middleware decorator storm orm dbms db postgres mysql sqlite web webdev www',
    author='Vsevolod Balashov',
    author_email='vsevolod@balashov.name',
    url='http://pypi.python.org/pypi/middlestorm',
    license='LGPL 2.1',
    py_modules=["middlestorm"],
    test_suite='nose.collector',
    install_requires=["storm>=0.10"],
    entry_points = """\
        [paste.filter_app_factory]
        middlestorm = middlestorm:make_middleware
        """,
    zip_safe=True
)
