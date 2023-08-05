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


from sqlalchemy import types, Column, PrimaryKeyConstraint
from sqlalchemy.sql.compiler import OPERATORS
from sqlalchemy.sql import operators as sql_operators

from sqlbase7_sa.sqlbase7 import SQLBase7Compiler, SQLBase7Dialect


class SQLBase7Compiler_SA05(SQLBase7Compiler):

    operators = SQLBase7Compiler.operators.copy()
    operators.update({
            sql_operators.ilike_op: lambda x, y, escape=None: "@lower(%s) LIKE @lower(%s)" % (x, y) + (escape and ' ESCAPE \'%s\'' % escape or ''),
            })


class SQLBase7Dialect_SA05(SQLBase7Dialect):

    statement_compiler = SQLBase7Compiler_SA05
    
    @classmethod
    def dbapi(cls):
        import pyodbc
        return pyodbc

    def table_names(self, connection, schema):
        cursor = connection.connection.cursor()
        table_names = [row.NAME for row in cursor.execute(
                "SELECT NAME FROM %s.SYSTABLES WHERE REMARKS IS NOT NULL" % schema
                )]
        cursor.close()
        return table_names

    def reflecttable(self, connection, table, include_columns=None):
        if table.schema is None:
            table.schema = connection.default_schema_name()

        sql = "SELECT NAME,COLTYPE,NULLS FROM %s.SYSCOLUMNS WHERE TBNAME = '%s'" % (table.schema, table.name)
        if include_columns:
            sql += " AND NAME NOT IN (%s)" % ','.join(include_columns)
        cursor = connection.connection.cursor()
        for row in cursor.execute(sql):
            table.append_column(Column(row.NAME, self._type_map[row.COLTYPE]))
        cursor.close()

        cursor = connection.connection.cursor()
        key_columns = [row.COLNAME for row in cursor.execute(
                "SELECT COLNAME FROM %s.SYSPKCONSTRAINTS WHERE NAME = '%s' ORDER BY PKCOLSEQNUM" % (table.schema, table.name)
                )]
        if key_columns:
            table.append_constraint(PrimaryKeyConstraint(*key_columns))
        cursor.close()
