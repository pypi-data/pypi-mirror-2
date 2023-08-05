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


from sqlbase7_sa.sqlbase7 import SQLBase7Compiler, SQLBase7Dialect

from sqlalchemy.connectors.pyodbc import PyODBCConnector


class SQLBase7Compiler_SA06(SQLBase7Compiler):

    def visit_ilike_op(self, binary, **kw):
        escape = binary.modifiers.get("escape", None)
        return '@lower(%s) LIKE @lower(%s)' % (
                                            self.process(binary.left, **kw), 
                                            self.process(binary.right, **kw)) \
            + (escape and ' ESCAPE \'%s\'' % escape or '')    


class SQLBase7Dialect_SA06(SQLBase7Dialect):

    statement_compiler = SQLBase7Compiler_SA06

    def _get_default_schema_name(self, connection):
        return 'SYSADM'

    def _check_unicode_returns(self, connection):
        return False

    def get_table_names(self, connection, schema=None, **kw):
        cursor = connection.connection.cursor()
        table_names = [row.NAME for row in cursor.execute(
                "SELECT NAME FROM %s.SYSTABLES WHERE REMARKS IS NOT NULL" % schema
                )]
        cursor.close()
        return table_names

    def get_columns(self, connection, table_name, schema=None, **kw):
        if schema is None:
            schema = self.get_default_schema_name(connection)
        cursor = connection.connection.cursor()
        columns = []

        for row in cursor.execute("SELECT NAME,COLTYPE,NULLS FROM %s.SYSCOLUMNS WHERE TBNAME = '%s'" % (schema, table_name)):

            columns.append({
                    'name'              : row.NAME,
                    'type'              : self._type_map[row.COLTYPE],
                    'nullable'          : row.NULLS == 'Y',
                    'default'           : None,
                    'autoincrement'     : False,
                    })

        cursor.close()
        return columns

    def get_primary_keys(self, connection, table_name, schema=None, **kw):
        if schema is None:
            schema = self.get_default_schema_name(connection)
        cursor = connection.connection.cursor()
        primary_keys = [row.COLNAME for row in cursor.execute(
                "SELECT COLNAME FROM %s.SYSPKCONSTRAINTS WHERE NAME = '%s' ORDER BY PKCOLSEQNUM" % (schema, table_name)
                )]
        cursor.close()
        return primary_keys

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []


class SQLBase7Dialect_SA06_pyodbc(SQLBase7Dialect_SA06, PyODBCConnector):
    pass


dialect = SQLBase7Dialect_SA06_pyodbc
