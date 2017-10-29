import pandas as pd
from tribble.transformers import schema_conformer


def test_column_rename():
    data = pd.DataFrame([{'id': 1, 'foo': 'data'}])
    renames = {
        'id': 'id',
        'foo': 'bar'
    }
    output = schema_conformer.SchemaConformer(renames).apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'bar': 'data'}
    ]


def test_column_drop():
    data = pd.DataFrame([{'id': 1, 'foo': 'bar'}])
    renames = {'id': 'id'}
    output = schema_conformer.SchemaConformer(renames).apply(data)
    assert output.to_dict('records') == [
        {'id': 1}
    ]
