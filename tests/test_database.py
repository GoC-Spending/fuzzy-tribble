from sqlalchemy import engine
from tribble import database

def test_connection(db_engine: engine.base.Engine) -> None:
    connection = db_engine.connect()
    result = connection.execute('SELECT 1;').fetchall()
    assert result == [(1,)]


def test_init(db_engine: engine.base.Engine) -> None:
    database.init(db_engine, force=True)
