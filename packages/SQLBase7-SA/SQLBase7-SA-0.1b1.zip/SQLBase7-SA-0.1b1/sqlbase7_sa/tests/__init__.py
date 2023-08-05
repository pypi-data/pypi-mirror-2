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


import unittest

from sqlalchemy import create_engine, MetaData


# NOTE:  This whole project exists for the sake of accessing legacy CAM32 databases,
# so it should come as no surprise that these tests are only expected to leverage
# such a specific database.  If you do not have a CAM32 database, or if yours
# happens to be set up in a non-standard way, etc., then you'll need to change the
# TestCase.setUp() method to reflect your environment.


class TestCase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlbase7://odbc:readonly@server1/cam32")


class ConnectionTestCase(TestCase):

    def runTest(self):
        connection = self.engine.connect()
        connection.close()


class ReflectionTestCase(TestCase):

    def runTest(self):
        metadata = MetaData(bind=self.engine, reflect=True)
        self.assert_(metadata.tables)
