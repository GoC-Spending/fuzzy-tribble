import datetime
import pandas as pd
from tribble.transformers import reporting_period_value


def test_apply() -> None:
    data = pd.DataFrame([
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 3, 31),
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 4, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
        }
    ])
    output = reporting_period_value.ReportingPeriodValue().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['reporting_period_start']) == [
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 3, 31),
            'reporting_period_value': 246575.34,
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 4, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
            'reporting_period_value': 753424.66,
        }
    ]


def test_apply_when_contract_ends_later() -> None:
    data = pd.DataFrame([
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 6, 30),
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 7, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
        }
    ])
    output = reporting_period_value.ReportingPeriodValue().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['reporting_period_start']) == [
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 6, 30),
            'reporting_period_value': 495890.41,
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 7, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
            'reporting_period_value': 168954.76,
        }
    ]


def test_apply_when_reporting_value_goes_negative() -> None:
    data = pd.DataFrame([
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 6, 30),
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 250000.00,
            'reporting_period_start': datetime.date(2014, 7, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
        }
    ])
    output = reporting_period_value.ReportingPeriodValue().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['reporting_period_start']) == [
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 1000000.00,
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 6, 30),
            'reporting_period_value': 495890.41,
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'contract_value': 250000.00,
            'reporting_period_start': datetime.date(2014, 7, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
            'reporting_period_value': -245890.41,
        }
    ]
