import typing
import mysql.connector


def test_connection(db_host: str, db_user: str, db_password: typing.Optional[str], db_name: str):
    connection = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    cursor.execute('SELECT 1;')
    assert list(cursor) == [(1,)]
