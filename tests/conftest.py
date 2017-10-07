import getpass
import os
import random
import typing
import pytest
from sqlalchemy import engine
from tribble import database


@pytest.fixture
def db_host() -> str:
    return os.environ.get('TRIBBLE_DB_HOST', 'localhost')


@pytest.fixture
def db_user() -> str:
    return os.environ.get('TRIBBLE_DB_USER', getpass.getuser())


@pytest.fixture
def db_password() -> typing.Optional[str]:
    return os.environ.get('TRIBBLE_DB_PASSWORD')


@pytest.fixture
def db_name(db_host: str, db_user: str) -> typing.Iterable[str]:
    admin_user = os.environ.get('TRIBBLE_DB_ADMIN_USER', 'root')
    admin_password = os.environ.get('TRIBBLE_DB_ADMIN_PASSWORD')

    creds = database.Creds(host=db_host, user=admin_user, password=admin_password, database='mysql')
    engine = database.connect_db(creds)

    connection = engine.connect()
    db_names = connection.execute('SHOW DATABASES;').fetchall()

    for (db_name,) in db_names:
        if db_name.startswith('tribble_test_'):
            engine.execute(f'DROP SCHEMA {db_name}')

    database_name = 'tribble_test_{0:0>6}'.format(random.randrange(1, 1000000))
    connection.execute(f'CREATE SCHEMA {database_name};')

    connection.execute(f'USE {database_name};')
    connection.execute(f'GRANT ALL ON {database_name}.* TO {db_user}@{db_host};')
    connection.execute('FLUSH PRIVILEGES;')

    connection.close()

    yield database_name

    connection = engine.connect()
    connection.execute(f'DROP SCHEMA {database_name};')
    connection.execute(f'REVOKE ALL ON {database_name}.* FROM {db_user}@{db_host};')
    connection.execute('FLUSH PRIVILEGES;')
    connection.close()


@pytest.fixture
def db_engine(db_host: str, db_user: str, db_password: str, db_name: str) -> engine.base.Engine:
    creds = database.Creds(host=db_host, user=db_user, password=db_password, database=db_name)
    return database.connect_db(creds)
