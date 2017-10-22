import typing
from sqlalchemy import create_engine, engine


class Creds(typing.NamedTuple):
    host: str
    user: str
    password: typing.Optional[str]
    database: str


def connect_db(creds: Creds) -> engine.base.Engine:
    password_stub = f':{creds.password}' if creds.password else ''
    return create_engine(f"mysql+mysqldb://{creds.user}{password_stub}@{creds.host}/{creds.database}")


def create_db(engine: engine.base.Engine, database_name: str, runtime_user: str, runtime_host: str,
              force: bool = False) -> None:
    connection = engine.connect()
    if force:
        connection.execute(f'DROP SCHEMA IF EXISTS {database_name};')
    connection.execute(f'CREATE SCHEMA {database_name};')
    connection.execute(f'GRANT ALL PRIVILEGES ON {database_name}.* to {runtime_user}@{runtime_host};')
    connection.execute('FLUSH PRIVILEGES;')
    connection.close()
