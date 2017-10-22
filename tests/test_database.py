from sqlalchemy import engine


def test_connection(db_engine: engine.base.Engine) -> None:
    connection = db_engine.connect()
    result = connection.execute('SELECT 1;').fetchall()
    assert result == [(1,)]
