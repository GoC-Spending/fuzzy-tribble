import getpass
import typing
import click
import tribble.database
import tribble.transform
from tribble import contract
from tribble import loader
from tribble import log
from tribble import reader


SPENDING_DB_NAME = 'spending'
LOGGER = log.get_logger(__name__)


@click.group()
@click.option('--host', default='localhost', help='MySQL hostname. This defaults to "localhost".')
@click.option('--user', default=getpass.getuser(), help='Username to connect to MySQL.')
@click.option('--password', help='Password for the provided username.')
@click.option('--schema', default=SPENDING_DB_NAME, help='Database name for tribble to work in.')
@click.pass_context
def main(ctx: click.core.Context, host: str, user: str, password: typing.Optional[str], schema: str) -> None:
    """Main entrypoint for fuzzy-tribble.

    Type --help after any subcommand for additional help."""
    ctx.obj = {}
    creds = tribble.database.Creds(host, user, password, schema)
    engine = tribble.database.connect_db(creds)
    contract.Session.configure(bind=engine)
    ctx.obj['creds'] = creds
    ctx.obj['engine'] = engine


@main.command()
@click.option('--runtime-user', default=getpass.getuser(), help='Runtime username for normal usage.')
@click.option('--runtime-host', default='localhost', help='Hostname for runtime user. Defaults to "localhost".')
@click.option('--force', type=bool, default=False, is_flag=True, help='Drop the database first if it exists.')
@click.pass_context
def create_db(ctx: click.core.Context, runtime_user: str, runtime_host: str, force: bool) -> None:
    """Create the database on MySQL.

    Needs to be run with admin privileges, e.g. `tribble --user root create_db`"""
    passed_creds = ctx.obj['creds']
    creds = tribble.database.Creds(host=passed_creds.host, user=passed_creds.user,
                                   password=passed_creds.password, database='mysql')
    engine = tribble.database.connect_db(creds)
    tribble.database.create_db(engine, passed_creds.database, runtime_user, runtime_host, force)


@main.command()
@click.option('--force', type=bool, default=False, is_flag=True, help='Drop all data first if the tables exist.')
@click.pass_context
def init_db(ctx: click.core.Context, force: bool) -> None:
    """Initialize the database, setting up all required tables.

    Use `--force` to re-initialize the database."""
    engine = ctx.obj['engine']
    if force:
        contract.Base.metadata.drop_all(engine)
    contract.Base.metadata.create_all(engine)


@main.command()
@click.argument('input-dir', type=click.Path(exists=True))
def load(input_dir: str) -> None:
    """Load data from scraped JSON files into the database.

    To download this data, first run `git clone https://github.com/GoC-Spending/goc-spending-data` in another folder."""
    raw_contracts = reader.read_dir(input_dir)
    contracts = tribble.transform.transform(raw_contracts)

    LOGGER.info(f'Loading data from {input_dir} in database.')
    print("Storing in db ...")
    loader.load_dataframe(raw_contracts, contract.RawContract)
    loader.load_dataframe(contracts, contract.Contract)
    print("Finished.")
    LOGGER.info('Finished loading data.')

