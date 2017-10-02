import getpass
import os
import random
import typing
import mysql.connector
import pytest


@pytest.fixture(scope='session')
def db_host() -> str:
    return os.environ.get('TRIBBLE_DB_HOST', 'localhost')


@pytest.fixture(scope='session')
def db_user() -> str:
    return os.environ.get('TRIBBLE_DB_USER', getpass.getuser())


@pytest.fixture(scope='session')
def db_password() -> typing.Optional[str]:
    return os.environ.get('TRIBBLE_DB_PASSWORD')


@pytest.fixture(scope='session')
def db_name(db_host: str, db_user: str) -> typing.Iterable[str]:
    admin_user = os.environ.get('TRIBBLE_DB_ADMIN_USER', 'root')
    admin_password = os.environ.get('TRIBBLE_DB_ADMIN_PASSWORD')

    connection = mysql.connector.connect(host=db_host, user=admin_user, password=admin_password, database='mysql')
    cursor = connection.cursor()

    cursor.execute('SHOW DATABASES;')
    db_names = list(cursor)

    for (db_name,) in db_names:
        if db_name.startswith('tribble_test_'):
            cursor.execute(f'DROP SCHEMA {db_name}')

    database_name = 'tribble_test_{0:0>6}'.format(random.randrange(1, 1000000))
    cursor.execute(f'CREATE SCHEMA {database_name};')

    cursor.execute(f'USE {database_name};')
    cursor.execute(f'GRANT ALL ON {database_name} TO {db_user}@{db_host};')
    cursor.execute('FLUSH PRIVILEGES;')

    cursor.close()
    connection.close()

    yield database_name

    connection = mysql.connector.connect(host=db_host, user=admin_user, password=admin_password, database='mysql')
    cursor = connection.cursor()

    cursor.execute(f'DROP SCHEMA {database_name}')
    cursor.close()
    connection.close()
