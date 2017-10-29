import datetime
import pandas as pd
from tribble.transformers import date_parser


def test_apply() -> None:
    data = pd.DataFrame([{'id': 1, 'data': '2017-01-01'}])
    output = date_parser.DateParser('data').apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'data': datetime.date(2017, 1, 1)}
    ]


def test_reversed_month_day() -> None:
    data = pd.DataFrame([{'id': 1, 'data': '2017-13-01'}])
    output = date_parser.DateParser('data').apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'data': datetime.date(2017, 1, 13)}
    ]


def test_non_date() -> None:
    data = pd.DataFrame([{'id': 1, 'data': 'foo'}])
    output = date_parser.DateParser('data').apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'data': None}
    ]


def test_bad_date() -> None:
    data = pd.DataFrame([{'id': 1, 'data': '2017-01-32'}])
    output = date_parser.DateParser('data').apply(data)
    assert output.to_dict('records') == [
        {'id': 1, 'data': None}
    ]
