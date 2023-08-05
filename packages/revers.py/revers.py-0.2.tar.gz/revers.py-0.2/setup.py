#!/usr/bin/env python
#
# $Id: setup.py,v a586707b80b1 2010/06/09 12:32:42 vsevolod $

from setuptools import setup

import reverstorm

setup(
    name='revers.py',
    version=reverstorm.__version__,
    description="Reverse Entity-Relationship Storm",
    long_description=open('README.rest').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
    ], 
    keywords='python storm reverse',
    author=reverstorm.__author__,
    author_email=reverstorm.__email__,
    url='http://pypi.python.org/pypi/revers',
    license='GPL 3',
    py_modules=["reverstorm"],
    test_suite='nose.collector',
    zip_safe=True,
    scripts=['revers.py'],
    install_requires=['storm']
)
