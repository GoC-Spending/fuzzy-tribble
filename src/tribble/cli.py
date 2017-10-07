import getpass
import os
import typing
import click
import tribble.database
import tribble.transform


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
@click.option('--schema', default='spending')
@click.pass_context
def database(ctx: click.core.Context, host: str, user: str, password: typing.Optional[str], schema: str) -> None:
    creds = tribble.database.Creds(host, user, password, schema)
    ctx.obj['creds'] = creds


@database.command()
@click.option('--force', type=bool, default=False, is_flag=True)
@click.pass_context
def init(ctx: click.core.Context, force: bool) -> None:
    tribble.database.init(ctx.obj['creds'], force)
