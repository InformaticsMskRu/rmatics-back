"""Lets the suite run on SQLite for quick local runs: SQLALCHEMY_DATABASE_URI=sqlite://

The models live in the moodle / pynformatics / ejudge schemas, so each one is attached as
its own database file in a temporary directory. File-backed (not :memory:) so that several
Flask apps created in one run share state, like they share a MariaDB server.
This does not replace a run against MariaDB. Known gaps: foreign keys are not enforced, so
ON DELETE CASCADE rows survive between tests and a reused id can hit a stale
language_contest row (test_problem_api languages tests).
"""
import os
import shutil
import sqlite3
import tempfile

from sqlalchemy import event
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.engine import Engine
from sqlalchemy.ext.compiler import compiles

SCHEMAS = ('moodle', 'pynformatics', 'ejudge')

_db_dir = None

if os.environ.get('SQLALCHEMY_DATABASE_URI') == 'sqlite://':
    _db_dir = tempfile.mkdtemp(prefix='rmatics-back-tests-')
    os.environ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_db_dir}/main.db'


def pytest_unconfigure(config):
    if _db_dir:
        shutil.rmtree(_db_dir, ignore_errors=True)


@event.listens_for(Engine, 'connect')
def attach_schemas(dbapi_connection, connection_record):
    if _db_dir is None or not isinstance(dbapi_connection, sqlite3.Connection):
        return
    for schema in SCHEMAS:
        dbapi_connection.execute(f"ATTACH DATABASE '{_db_dir}/{schema}.db' AS {schema}")
    # Recipe from the SQLAlchemy docs: pysqlite otherwise mishandles SAVEPOINT.
    dbapi_connection.isolation_level = None


@event.listens_for(Engine, 'begin')
def emit_begin(connection):
    if _db_dir is not None and connection.dialect.name == 'sqlite':
        connection.exec_driver_sql('BEGIN')


@compiles(MEDIUMTEXT, 'sqlite')
def compile_mediumtext(element, compiler, **kw):
    return 'TEXT'
