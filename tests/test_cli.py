import json
import pytest
import py._path.local
import click.testing
from sqlalchemy import engine
from tribble import cli
from tribble import contract


@pytest.mark.usefixtures('db')
def test_load(tmpdir: py._path.local.LocalPath) -> None:
    input_dir = tmpdir.mkdir('input')
    data_file = input_dir.join('data.json')
    data_file.write(json.dumps({'uuid': 'foo'}))

    runner = click.testing.CliRunner()  # type: ignore
    result = runner.invoke(cli.load, [str(input_dir)])
    assert result.exit_code == 0

    session = contract.Session()
    contracts = list(session.query(contract.Contract))
    session.close()

    expected = [contract.Contract(id=1, uuid='foo')]
    assert contracts == expected


def test_init_db(db_engine: engine.base.Engine) -> None:
    connection = db_engine.connect()
    tables = connection.execute("SHOW TABLES LIKE 'contracts';").fetchall()
    assert not tables

    runner = click.testing.CliRunner()  # type: ignore
    result = runner.invoke(cli.init_db, obj={'engine': db_engine})

    assert result.exit_code == 0

    tables = connection.execute("SHOW TABLES LIKE 'contracts';").fetchall()
    assert len(tables) == 1


def test_init_db_with_force(db_engine: engine.base.Engine) -> None:
    connection = db_engine.connect()
    connection.execute("CREATE TABLE contracts (foo INT NOT NULL)")
    table_def = connection.execute("SHOW CREATE TABLE contracts;").fetchall()[0][1]
    assert 'foo' in table_def

    runner = click.testing.CliRunner()  # type: ignore
    result = runner.invoke(cli.init_db, ['--force'], obj={'engine': db_engine})

    assert result.exit_code == 0

    table_def = connection.execute("SHOW CREATE TABLE contracts;").fetchall()[0][1]
    assert 'foo' not in table_def
    assert 'uuid' in table_def
