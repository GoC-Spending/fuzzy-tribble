import json
import py
from tribble import reader


def test_chunking(tmpdir: py._path.local.LocalPath) -> None:
    for i in range(0, 100):
        data = {'uuid': 'tbs-{}'.format(i)}
        data_file = tmpdir.join('data{}.json'.format(i))
        data_file.write(json.dumps(data))

    output = reader.read_dir(str(tmpdir), grouping_length=7)
    assert len(output) == 100


def test_blank_dir(tmpdir: py._path.local.LocalPath) -> None:
    output = reader.read_dir(str(tmpdir))
    assert len(output) == 0  # pylint: disable=len-as-condition
