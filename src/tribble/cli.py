import getpass
import os
import typing
import click
import tribble.database
import tribble.transform


SPENDING_DB_NAME = 'spending'


@click.group()
@click.pass_context
def main(ctx: click.core.Context) -> None:
    ctx.obj = {}


@main.command()
@click.argument('input-dir')
@click.option('--output', required=True)
def transform(input_dir: str, output: str) -> None:
    assert os.path.exists(os.path.dirname(output)), "output directory must already exist"

    df = tribble.transform.transform_dir(input_dir)
    df.to_csv(output)


@main.group()
@click.option('--host', default='localhost')
@click.option('--user', default=getpass.getuser())
@click.option('--password')
@click.option('--schema', default=SPENDING_DB_NAME)
@click.pass_context
def database(ctx: click.core.Context, host: str, user: str, password: typing.Optional[str], schema: str) -> None:
    creds = tribble.database.Creds(host, user, password, schema)
    ctx.obj['creds'] = creds


@database.command()
@click.option('--runtime-user', default=getpass.getuser())
@click.option('--runtime-host', default='localhost')
@click.option('--force', type=bool, default=False, is_flag=True)
@click.pass_context
def create(ctx: click.core.Context, runtime_user: str, runtime_host: str, force: bool) -> None:
    passed_creds = ctx.obj['creds']
    creds = tribble.database.Creds(host=passed_creds.host, user=passed_creds.user,
                                   password=passed_creds.password, database='mysql')
    engine = tribble.database.connect_db(creds)
    tribble.database.create_db(engine, passed_creds.database, runtime_user, runtime_host, force)


@database.command()
@click.option('--force', type=bool, default=False, is_flag=True)
@click.pass_context
def init(ctx: click.core.Context, force: bool) -> None:
    engine = tribble.database.connect_db(ctx.obj['creds'])
    tribble.database.init(engine, force)
