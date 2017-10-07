import typing
from sqlalchemy import create_engine, MetaData, Table, Column, VARCHAR, TEXT


class Creds(typing.NamedTuple):
    host: str
    user: str
    password: typing.Optional[str]
    database: str


def init(creds: Creds, force: bool) -> None:
    password_stub = f':{creds.password}' if creds.password else ''
    engine = create_engine(f"mysql+mysqldb://{creds.user}{password_stub}@{creds.host}/{creds.database}")
    meta = MetaData(bind=engine)

    spending = Table('spending', meta,
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

    if force:
        spending.drop(engine)
    spending.create(engine)
