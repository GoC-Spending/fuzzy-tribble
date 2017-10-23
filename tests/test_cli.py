import json
import pytest
import py._path.local
import click.testing
from sqlalchemy import engine
from tribble import cli
from tribble import contract


@pytest.fixture
def input_dir(tmpdir: py._path.local.LocalPath) -> py._path.local.LocalPath:
    return tmpdir.mkdir('input')


@pytest.fixture
def data_file(input_dir: py._path.local.LocalPath) -> str:
    data_file = input_dir.join('data.json')
    data_file.write(json.dumps({
        "uuid": "tbs-0000000000",
        "vendorName": "ABC Company",
        "referenceNumber": "0000000000",
        "contractDate": "2012â03â31",
        "description": "499 OTHER PROFESSIONAL SERVICES NOT ELSEWHERE SPECIFIED",
        "extraDescription": "Big Contract #1",
        "objectCode": "0499",
        "contractPeriodStart": "2012-04-01",
        "contractPeriodEnd": "2018-03-31",
        "startYear": "2012",
        "endYear": "2018",
        "deliveryDate": "",
        "originalValue": 6000.0,
        "contractValue": 6000,
        "comments": "This contract includes one or more amendments.This contract was competitively sourced." +
                    "This contract is a multi-year contract.",
        "ownerAcronym": "tbs",
        "sourceYear": 2012,
        "sourceQuarter": 1,
        "sourceFiscal": "201213-Q4",
        "sourceFilename": r"tbs\/5ae78038dd512ae3f7e8a91349f443cb.html",
        "sourceURL": r"http:\/\/www.tbs-sct.gc.ca\/scripts\/contracts-contrats\/reports-rapports-eng.asp" +
                     "?r=c&refNum=0000000000&q=4&yr=2012&d=",
        "amendedValues": [],
        "contractPeriodRange": "2012-04-01 to 2018-03-31",
        "yearsDuration": 6,
        "valuePerYear": 1000.0,
        "vendorClean": "Big Contract #1"
    }))
    return str(data_file)


@pytest.mark.usefixtures('db', 'data_file')
def test_load(input_dir: py._path.local.LocalPath) -> None:
    runner = click.testing.CliRunner()  # type: ignore
    result = runner.invoke(cli.load, [str(input_dir)])
    assert result.exit_code == 0

    session = contract.Session()
    contracts = list(session.query(contract.Contract))
    session.close()

    assert len(contracts) == 1
    assert contracts[0].uuid == 'tbs-0000000000'


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
