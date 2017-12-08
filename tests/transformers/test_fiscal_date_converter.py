import datetime
import pandas as pd
from tribble.transformers import fiscal_date_converter


def test_conversion() -> None:
    data = pd.DataFrame([
        {'id': 1, 'data': '201314-Q1'},
        {'id': 2, 'data': '201314-Q4'},
    ])
    output = fiscal_date_converter.FiscalDateConverter('data').apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['id']) == [
        {'id': 1, 'data': datetime.date(2013, 4, 1)},
        {'id': 2, 'data': datetime.date(2014, 1, 1)},
    ]


def test_bad_data() -> None:
    data = pd.DataFrame([
        {'id': 1, 'data': '201314-Q5'},
        {'id': 2, 'data': '201315-Q1'},
        {'id': 3, 'data': 'foo'},
    ])
    output = fiscal_date_converter.FiscalDateConverter('data').apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['id']) == [
        {'id': 1, 'data': None},
        {'id': 2, 'data': None},
        {'id': 3, 'data': None},
    ]


def test_removes_blank_fiscal_date() -> None:
    data = pd.DataFrame([
        {'id': 1, 'data': None},
        {'id': 2, 'data': datetime.date(2012, 4, 1)}
    ])

    output = fiscal_date_converter.BlankFiscalDateFilter('data').apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['id']) == [
        {'id': 2, 'data': datetime.date(2012, 4, 1)},
    ]
