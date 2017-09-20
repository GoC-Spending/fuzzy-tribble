import json
import os
import py._path.local
import click.testing
from tribble import cli


def test_transform(tmpdir: py._path.local.LocalPath) -> None:
    input_dir = tmpdir.mkdir('input')
    data_file = input_dir.join('data.json')
    data_file.write(json.dumps({'a': 1, 'b': 'foo'}))

    output_filename = '{}/{}'.format(str(tmpdir), 'output.csv')

    runner = click.testing.CliRunner()  # type: ignore
    result = runner.invoke(cli.transform, [str(input_dir), '--output', output_filename])
    assert result.exit_code == 0

    assert os.path.exists(output_filename)
    with open(output_filename) as result_file:
        data = result_file.readlines()
        assert data == [
            ',a,b\n',
            '0,1,foo\n'
        ]
