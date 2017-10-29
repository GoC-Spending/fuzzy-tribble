import pandas as pd
from tribble.transformers import clear_blanks


def test_apply() -> None:
    data = pd.DataFrame([
        {'id': 1, 'data': ''},
        {'id': 2, 'data': None},
        {'id': 3, 'data': 'foo'},
    ])
    output = clear_blanks.ClearBlanks('data').apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['id']) == [
        {'id': 1, 'data': None},
        {'id': 2, 'data': None},
        {'id': 3, 'data': 'foo'},
    ]


def test_multiple_columns() -> None:
    data = pd.DataFrame([
        {'id': 1, 'foo': '', 'bar': '', 'baz': 'data'}
    ])
    output = clear_blanks.ClearBlanks('foo', 'bar', 'baz').apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'foo': None, 'bar': None, 'baz': 'data'}
    ]
