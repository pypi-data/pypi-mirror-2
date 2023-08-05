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


from sqlalchemy.connectors.pyodbc import PyODBCConnector

from sqlbase7_sa.base import SQLBase7Dialect


class SQLBase7_pyodbc(PyODBCConnector, SQLBase7Dialect):

    def create_connect_args(self, url):
        connection_string = ';'.join((
                "DRIVER={Centura SQLBase 3.5 32-bit Driver -NT & Win95}",
                "SERVER=%s" % url.host,
                "DATABASE=%s" % url.database,
                "UID=%s" % url.username,
                "PWD=%s" % url.password,
                ))
        return [connection_string], {}


dialect = SQLBase7_pyodbc
