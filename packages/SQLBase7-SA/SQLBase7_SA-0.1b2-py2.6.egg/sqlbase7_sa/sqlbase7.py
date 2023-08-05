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
from sqlalchemy.sql.expression import Join


import sqlalchemy
from pkg_resources import parse_version
if parse_version(sqlalchemy.__version__) <= parse_version('0.5.99'):
    from sqlalchemy.sql.compiler import DefaultCompiler as CompilerBase
else:
    from sqlalchemy.sql.compiler import SQLCompiler as CompilerBase


class LimitClauseNotSupported(Exception):

    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    def __str__(self):
        return "Centura SQLBase 7.5.1 doesn't support a LIMIT clause for the SELECT statement (received: limit = %u, offset = %u)" % (self.limit, self.offset)


class SQLBase7Compiler(CompilerBase):

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
        return super(SQLBase7Compiler, self).visit_select(select, **kwargs)

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


class SQLBase7Dialect(DefaultDialect):
    
    name = 'sqlbase7'

    statement_compiler = SQLBase7Compiler

    max_identifier_length = 18

    _type_map = {
        'CHAR'          : types.CHAR,
        'DATE'          : types.DATE,
        'DECIMAL'       : types.DECIMAL,
        'FLOAT'         : types.FLOAT,
        'SMALLINT'      : types.SMALLINT,
        'TIME'          : types.TIME,
        'TIMESTMP'      : types.TIMESTAMP,
        'VARCHAR'       : types.VARCHAR,
        }

    def create_connect_args(self, url):
        connection_string = ';'.join((
                "DRIVER={Centura SQLBase 3.5 32-bit Driver -NT & Win95}",
                "SERVER=%s" % url.host,
                "DATABASE=%s" % url.database,
                "UID=%s" % url.username,
                "PWD=%s" % url.password,
                ))
        return [connection_string], {}

    def get_default_schema_name(self, connection):
        return 'SYSADM'
    
    def do_execute(self, cursor, statement, parameters, context=None):
        # For some (perhaps good?) reason, the SQLBase ODBC driver doesn't like
        # parameters if they're of Unicode or Long type.  I'd hoped at first that
        # the "supports_unicode_binds" attribute would take care of the Unicode
        # problem but it didn't seem to.  And now the Long parameters seem to
        # throw the same error, so...
        parameters = list(parameters)
        for i, parameter in enumerate(parameters):
            if isinstance(parameter, unicode):
                parameters[i] = str(parameter)
            elif isinstance(parameter, long):
                parameters[i] = int(parameter)
        super(SQLBase7Dialect, self).do_execute(cursor, statement, tuple(parameters), context)
