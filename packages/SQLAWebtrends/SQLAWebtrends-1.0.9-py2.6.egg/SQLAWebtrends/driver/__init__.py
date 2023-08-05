# -*- coding: utf-8 -*-

"""Webtrends ODBC dialect for SQLAlchemy
"""
__author__ = 'Wes Mason <wes.mason@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '1.0.8'

import sys
import urllib
from sqlalchemy import types as sqltypes
from sqlalchemy.connectors.pyodbc import PyODBCConnector
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.engine import reflection
from sqlalchemy.util import asbool
from sqlalchemy.sql import compiler


SCHEMA_NAMES = {
    'BINARY': sqltypes.BLOB,
    'VARBINARY': sqltypes.BLOB,
    'BYTEA': sqltypes.BLOB,
    'RAW': sqltypes.BLOB,

    'BOOLEAN': sqltypes.BOOLEAN,

    'CHAR': sqltypes.CHAR,
    'VARCHAR': sqltypes.VARCHAR,
    'VARCHAR2': sqltypes.VARCHAR,

    'DATE': sqltypes.DATE,
    'DATETIME': sqltypes.DATETIME,
    'SMALLDATETIME': sqltypes.DATETIME,
    'TIME': sqltypes.TIME,
    # Not supported yet
    # TIME WITH TIMEZONE
    # TIMESTAMP
    # TIMESTAMP WITH TIMEZONE
    # INTERVAL

    # All the same internal representation
    'FLOAT': sqltypes.FLOAT,
    'FLOAT8': sqltypes.FLOAT,
    'DOUBLE': sqltypes.FLOAT,
    'REAL': sqltypes.FLOAT,

    'INT': sqltypes.INTEGER,
    'INTEGER': sqltypes.INTEGER,
    'INT8': sqltypes.INTEGER,
    'BIGINT': sqltypes.INTEGER,
    'SMALLINT': sqltypes.INTEGER,
    'TINYINT': sqltypes.INTEGER,

    'NUMERIC': sqltypes.NUMERIC,
    'DECIMAL': sqltypes.NUMERIC,
    'NUMBER': sqltypes.NUMERIC,
    'MONEY': sqltypes.NUMERIC,
}


class WebtrendsConnection(PyODBCConnector):
    unicode_type = (sys.maxunicode < 2 ** 16) and 'UCS2' or 'UCS4'

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username='user')
        opts.update(url.query)

        keys = opts
        query = url.query

        connect_args = {}
        for param in ('ansi', 'unicode_results', 'autocommit'):
            if param in keys:
                connect_args[param] = asbool(keys.pop(param))

        if 'odbc_connect' in keys:
            connectors = [urllib.unquote_plus(keys.pop('odbc_connect'))]
        else:
            # Default Webtrends port:
            port = '80'
            if 'port' in keys and not 'port' in query:
                port = '%d' % int(keys.pop('port'))

            database = keys.pop('database', None)
            profile_guid = query.pop('profile_guid', '')
            connectors = [
                'SERVER=%s' % keys.pop('host', ''),
                'SSL=0',
                'PORT=%s' % (port,),
                'DATABASE=%s' % database,
                'AccountID=1',
            ]
            if database != 'WTSystem' and profile_guid:
                connectors.append('ProfileGuid=%s' % profile_guid)
            if 'dsn' in query:
                connectors.append(
                    "Extended Properties=DSN=%s" % query.pop('dsn', 'Webtrends')
                )

            user = keys.pop("user", None)
            if user:
                connectors.append("User ID=%s" % user)
                connectors.append("UID=%s" % user)
                connectors.append("PASSWORD=%s" % keys.pop('password', ''))

            connectors.extend(['%s=%s' % (k, v) for k, v in keys.iteritems()])

        return [[";".join (connectors)], connect_args]


class WebtrendsDialect(WebtrendsConnection, DefaultDialect):
    name = 'webtrends'
    ischema_names = SCHEMA_NAMES

    supports_alter = False
    supports_unicode = False
    supports_unicode_statements = False
    supports_unicode_binds = False
    supports_default_values = False
    supports_empty_insert = False
    supports_cast = False
    convert_unicode = True
    postfetch_lastrowid = False
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False

    def __init__(self, **params):
        super(WebtrendsDialect, self).__init__(**params)

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        return [row.table_name for row in connection.tables()]


    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        columns = []
        for row in connection.columns(table=table_name):
            columns.append({
                'name' : row.column_name,
                'type' : self.ischema_names[row.data_type.upper()],
                'nullable' : row.is_nullable,
                'default' : row.column_def,
                'primary_key': False,
            })
        return columns

    def _check_unicode_returns(self, connection):
        return False

    def do_rollback(self, connection):
        pass

    def do_execute(self, cursor, statement, parameters, context=None):
        # PyODBC fails at parsing a prepared statement for Webtrends
        # so unprepare it
        sql = statement
        if '?' in statement:
            parts = statement.split('?')
            sql = ""
            for i, part in enumerate(parts[:-1]):
                sql = "%s%s'%s'" % (sql, part, str(parameters[i]))
            sql = "%s%s" % (sql, parts[-1])
        cursor.execute(sql)

class WebtrendsIdentifierPreparer(compiler.IdentifierPreparer):
    def __init__(self, dialect):
        super(WebtrendsIdentifierPreparer, self).__init__(
            dialect,
            initial_quote='',
            final_quote=''
        )

class WebtrendsCompiler(compiler.SQLCompiler):
    def limit_clause(self, select):
        text = ""
        if select._limit is not None:
            text +=  " \n LIMIT " + str(select._limit)
        if select._offset:
            if select._limit is None:
                text = "\n LIMIT 0"
            text += ", " + str(select._offset)
        return text

dialect = WebtrendsDialect
dialect.preparer = WebtrendsIdentifierPreparer
dialect.statement_compiler = WebtrendsCompiler
