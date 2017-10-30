import datetime
import pandas as pd
from tribble.transformers import reporting_periodizer


def test_apply() -> None:
    data = pd.DataFrame([
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2014, 1, 1),
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2015, 1, 1),
        }
    ])
    output = reporting_periodizer.ReportingPeriodizer().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['contract_period_start']) == [
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2014, 1, 1),
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2014, 12, 31),
        }, {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2015, 1, 1),
            'reporting_period_start': datetime.date(2015, 1, 1),
            'reporting_period_end': datetime.date(2015, 12, 31),
        }
    ]


def test_single_item() -> None:
    data = pd.DataFrame([
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2014, 1, 1),
        }
    ])
    output = reporting_periodizer.ReportingPeriodizer().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['contract_period_start']) == [
        {
            'uuid': 1,
            'contract_period_start': datetime.date(2014, 1, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2014, 1, 1),
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2015, 12, 31),
        }
    ]
