import os
import click
import tribble.transform


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument('input-dir')
@click.option('--output', required=True)
def transform(input_dir: str, output: str) -> None:
    assert os.path.exists(os.path.dirname(output)), "output directory must already exist"

    df = tribble.transform.transform_dir(input_dir)
    df.to_csv(output)
