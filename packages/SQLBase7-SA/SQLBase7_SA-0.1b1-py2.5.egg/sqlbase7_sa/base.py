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


from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy import types, and_
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import Join


class LimitClauseNotSupported(Exception):

    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    def __str__(self):
        return "Centura SQLBase 7.5.1 doesn't support a LIMIT clause for the SELECT statement (received: limit = %u, offset = %u)" % (self.limit, self.offset)


class SQLBase7Compiler(SQLCompiler):

    # Most of the code below was copied from the Oracle dialect.  Thanks to Michael Bayer
    # for pointing that out.  Oh, and for writing SQLAlchemy; that was pretty cool.

    def visit_join(self, join, **kwargs):
        kwargs['asfrom'] = True
        return self.process(join.left, **kwargs) + ", " + self.process(join.right, **kwargs)

    def visit_select(self, select, **kwargs):
        froms = select._get_display_froms()
        whereclause = self._get_join_whereclause(froms)
        if whereclause is not None:
            select = select.where(whereclause)

        if select._limit is not None or select._offset is not None:
            raise LimitClauseNotSupported(select._limit, select._offset)

        kwargs['iswrapper'] = getattr(select, '_is_wrapper', False)
        return SQLCompiler.visit_select(self, select, **kwargs)

    def _get_join_whereclause(self, froms):
        clauses = []

        def visit_join(join):
            clauses.append(join.onclause)
            for j in join.left, join.right:
                if isinstance(j, Join):
                    visit_join(j)
                
        for f in froms:
            if isinstance(f, Join):
                visit_join(f)

        if clauses:
            return and_(*clauses)
        return None

    def visit_ilike_op(self, binary, **kw):
        escape = binary.modifiers.get("escape", None)
        return '@lower(%s) LIKE @lower(%s)' % (
                                            self.process(binary.left, **kw), 
                                            self.process(binary.right, **kw)) \
            + (escape and ' ESCAPE \'%s\'' % escape or '')

 
class SQLBase7Dialect(DefaultDialect):

    name = 'sqlbase7'

    max_identifier_length = 18

    # # Hmm, it'd be great if these actually did something...
    # supports_unicode_statements = False
    # supports_unicode_binds = False

    statement_compiler = SQLBase7Compiler

    type_map = {
        'CHAR'          : types.CHAR,
        'DATE'          : types.DATE,
        'DECIMAL'       : types.DECIMAL,
        'FLOAT'         : types.FLOAT,
        'SMALLINT'      : types.SMALLINT,
        'TIME'          : types.TIME,
        'TIMESTMP'      : types.TIMESTAMP,
        'VARCHAR'       : types.VARCHAR,
        }

    def _check_unicode_returns(self, connection):
        return False

    def get_table_names(self, connection, schema=None, **kw):
        if schema is None:
            schema = ''
        else:
            schema = '%s.' % schema

        cursor = connection.connection.cursor()
        table_names = [row.NAME for row in cursor.execute(
                "SELECT NAME FROM %sSYSTABLES WHERE REMARKS IS NOT NULL" % schema
                )]
        cursor.close()
        return table_names

    def get_columns(self, connection, table_name, schema=None, **kw):
        if schema is None:
            schema = ''
        else:
            schema = '%s.' % schema

        cursor = connection.connection.cursor()
        columns = []

        for row in cursor.execute("SELECT NAME,COLTYPE,NULLS FROM %sSYSCOLUMNS WHERE TBNAME = '%s'" % (schema, table_name)):

            columns.append({
                    'name'              : row.NAME,
                    'type'              : self.type_map[row.COLTYPE],
                    'nullable'          : row.NULLS == 'Y',
                    'default'           : None,
                    'autoincrement'     : False,
                    })

        cursor.close()
        return columns

    def get_primary_keys(self, connection, table_name, schema=None, **kw):
        if schema is None:
            schema = ''
        else:
            schema = '%s.' % schema

        cursor = connection.connection.cursor()
        primary_keys = [row.COLNAME for row in cursor.execute(
                "SELECT COLNAME FROM %sSYSPKCONSTRAINTS WHERE NAME = '%s' ORDER BY PKCOLSEQNUM" % (schema, table_name)
                )]
        cursor.close()
        return primary_keys

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def do_execute(self, cursor, statement, parameters, context=None):
        # For some (perhaps good?) reason, the SQLBase ODBC driver doesn't like
        # parameters if they're of Unicode or Long type.  I'd hoped at first that
        # the "supports_unicode_binds" attribute would take care of the Unicode
        # problem but it didn't seem to.  And now that the Long parameters seem
        # to throw the same error, so...
        _parameters = []
        for parameter in parameters:
            if isinstance(parameter, unicode):
                parameter = str(parameter)
            elif isinstance(parameter, long):
                parameter = int(parameter)
            _parameters.append(parameter)
        parameters = tuple(_parameters)
        cursor.execute(statement, parameters)
