import typing
from sqlalchemy import create_engine, MetaData, Table, Column, VARCHAR, TEXT, engine


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


def init(engine: engine.base.Engine, force: bool) -> None:
    meta = MetaData(bind=engine)

    contracts = Table('contracts', meta,
                      Column('uuid', VARCHAR(length=255), primary_key=True, autoincrement=False),
                      Column('vendor_name', TEXT, nullable=True),
                      Column('reference_number', TEXT, nullable=True),
                      Column('contract_date', VARCHAR(length=255), nullable=True),
                      Column('contract_period_start', VARCHAR(length=255), nullable=True),
                      Column('contract_period_end', VARCHAR(length=255), nullable=True),
                      Column('delivery_date', VARCHAR(length=255), nullable=True),
                      Column('contract_value', VARCHAR(length=255), nullable=True),
                      Column('department', TEXT, nullable=True),
                      Column('source_fiscal', VARCHAR(length=255), nullable=True)
                     )

    if force and contracts.exists():
        contracts.drop(engine)
    contracts.create(engine)
