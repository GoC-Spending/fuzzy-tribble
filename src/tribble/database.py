import contextlib
import typing
import mysql.connector
from mysql.connector import cursor as mysql_cursor
from mysql.connector import errorcode


class Creds(typing.NamedTuple):
    host: str
    user: str
    password: typing.Optional[str]
    database: str


@contextlib.contextmanager
def cursor(creds: Creds) -> mysql_cursor.MySQLCursor:
    connection: typing.Optional[mysql.connector.MySQLConnection] = None
    cursor_ = None
    try:
        connection = mysql.connector.connect(**creds._asdict())
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access Denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {} does not exist".format(creds.database))
        else:
            print("Unknown error: {}".format(err.msg))
    else:
        cursor_ = connection.cursor()
        yield cursor_
    finally:
        if cursor_:
            cursor_.close()
        if connection:
            connection.close()


def create_table(cursor_: mysql_cursor.MySQLCursor) -> None:
    cursor_.execute(
        "CREATE TABLE contracts ("
        "  uuid VARCHAR(50), "
        "  vendor_name VARCHAR(255), "
        "  reference_number VARCHAR(255), "
        "  contract_date VARCHAR(20), "
        "  contract_period_start VARCHAR(20), "
        "  contract_period_end VARCHAR(20), "
        "  delivery_date VARCHAR(20), "
        "  contract_value VARCHAR(255), "
        "  department VARCHAR(20), "
        "  source_fiscal VARCHAR(20)"
        ");"
    )


def drop_table(cursor_: mysql_cursor.MySQLCursor) -> None:
    cursor_.execute('DROP TABLE IF EXISTS contracts;')
