#!/usr/bin/env python
# -*- coding: utf-8  -*-
################################################################################
#
#  SQLBase7-SA -- SQLAlchemy driver/dialect for Centura SQLBase v7
#  Copyright © 2010 Lance Edgar
#
#  This file is part of SQLBase7-SA.
#
#  SQLBase7-SA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SQLBase7-SA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SQLBase7-SA.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


from setuptools import setup, find_packages


import os
execfile(os.path.join(os.path.dirname(__file__), 'sqlbase7_sa', '_version.py'))


setup(
    name = 'SQLBase7-SA',
    version = __version__,
    author = 'Lance Edgar',
    author_email = 'lance@edbob.org',
    url = "http://sqlbase7-sa.edbob.org/",
    license = "GNU GPL v3",
    description = 'SQLAlchemy dialect for Centura SQLBase v7',
    long_description = """
SQLBase7-SA - SQLAlchemy dialect for Centura SQLBase v7
-------------------------------------------------------

This package provides a (possibly rudimentary) implementation
of a SQLAlchemy dialect for the Centura SQLBase database
engine.  It is only intended (and known) to work with a very
specific version of this database, that version being 7.5.1.
""",

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

    packages = find_packages(),

    install_requires = [
        'SQLAlchemy',
        ],

    entry_points = {

        # SQLAlchemy 0.5
        'sqlalchemy.databases' : [
            'sqlbase7 = sqlbase7_sa.sqlbase7_sa05:SQLBase7Dialect_SA05',
            ],
        
        # SQLAlchemy 0.6
        'sqlalchemy.dialects' : [
            'sqlbase7 = sqlbase7_sa.sqlbase7_sa06:SQLBase7Dialect_SA06_pyodbc',
            ],
        },

    test_suite = 'sqlbase7_sa.tests',
    )
