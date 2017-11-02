import getpass
import typing
import click
import tribble.database
import tribble.transform
from tribble import contract
from tribble import loader
from tribble import reader


SPENDING_DB_NAME = 'spending'


@click.group()
@click.option('--host', default='localhost')
@click.option('--user', default=getpass.getuser())
@click.option('--password')
@click.option('--schema', default=SPENDING_DB_NAME)
@click.pass_context
def main(ctx: click.core.Context, host: str, user: str, password: typing.Optional[str], schema: str) -> None:
    ctx.obj = {}
    creds = tribble.database.Creds(host, user, password, schema)
    engine = tribble.database.connect_db(creds)
    contract.Session.configure(bind=engine)
    ctx.obj['creds'] = creds
    ctx.obj['engine'] = engine


@main.command()
@click.option('--runtime-user', default=getpass.getuser())
@click.option('--runtime-host', default='localhost')
@click.option('--force', type=bool, default=False, is_flag=True)
@click.pass_context
def create_db(ctx: click.core.Context, runtime_user: str, runtime_host: str, force: bool) -> None:
    passed_creds = ctx.obj['creds']
    creds = tribble.database.Creds(host=passed_creds.host, user=passed_creds.user,
                                   password=passed_creds.password, database='mysql')
    engine = tribble.database.connect_db(creds)
    tribble.database.create_db(engine, passed_creds.database, runtime_user, runtime_host, force)


@main.command()
@click.option('--force', type=bool, default=False, is_flag=True)
@click.pass_context
def init_db(ctx: click.core.Context, force: bool) -> None:
    engine = ctx.obj['engine']
    if force:
        contract.Base.metadata.drop_all(engine)
    contract.Base.metadata.create_all(engine)


@main.command()
@click.argument('input-dir')
def load(input_dir: str) -> None:
    raw_contracts = reader.read_dir(input_dir)
    contracts = tribble.transform.transform(raw_contracts)

    loader.load_dataframe(raw_contracts, contract.RawContract)
    loader.load_dataframe(contracts, contract.Contract)
