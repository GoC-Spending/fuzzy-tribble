import datetime
import typing
import pandas as pd
import pytest
from tribble.transformers import contract_date_cleaner


@pytest.fixture
def template() -> typing.Dict:
    return {
        'contract_period_start': None,
        'contract_period_end': None,
        'delivery_date': None,
        'contract_date': None,
        'source_fiscal': datetime.date(2017, 1, 1),
    }


def test_good_data(template: typing.Dict) -> None:
    template.update({'contract_period_start': datetime.date(2017, 1, 1),
                     'contract_period_end': datetime.date(2017, 2, 1)})
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': datetime.date(2017, 1, 1),
        'contract_period_start': datetime.date(2017, 1, 1),
        'contract_period_end': datetime.date(2017, 2, 1),
        'source_fiscal': datetime.date(2017, 1, 1),
    }]


def test_missing_end_date(template: typing.Dict) -> None:
    template.update({'contract_period_start': datetime.date(2017, 1, 1)})
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': datetime.date(2017, 1, 1),
        'contract_period_start': datetime.date(2017, 1, 1),
        'contract_period_end': datetime.date(2017, 1, 1),
        'source_fiscal': datetime.date(2017, 1, 1),
    }]


def test_delivery_date(template: typing.Dict) -> None:
    delivery_date = datetime.date(2017, 1, 1)
    template.update({'delivery_date': delivery_date})
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': datetime.date(2017, 1, 1),
        'contract_period_start': delivery_date,
        'contract_period_end': delivery_date,
        'source_fiscal': datetime.date(2017, 1, 1),
    }]


def test_contract_date(template: typing.Dict) -> None:
    contract_date = datetime.date(2017, 1, 1)
    template.update(({'contract_date': contract_date}))
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': contract_date,
        'contract_period_start': contract_date,
        'contract_period_end': contract_date,
        'source_fiscal': datetime.date(2017, 1, 1),
    }]


def test_no_dates(template: typing.Dict) -> None:
    fiscal_date = datetime.date(2017, 1, 1)
    template.update({'source_fiscal': fiscal_date})
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': fiscal_date,
        'contract_period_start': fiscal_date,
        'contract_period_end': fiscal_date,
        'source_fiscal': fiscal_date,
    }]


def test_contract_date_and_contract_period_end(template: typing.Dict) -> None:
    template.update({
        'contract_date': datetime.date(2017, 2, 1),
        'contract_period_end': datetime.date(2017, 3, 15),
    })
    data = pd.DataFrame([template])
    output = contract_date_cleaner.ContractDateCleaner().apply(data)
    assert output.to_dict('records') == [{
        'contract_date': datetime.date(2017, 2, 1),
        'contract_period_start': datetime.date(2017, 2, 1),
        'contract_period_end': datetime.date(2017, 3, 15),
        'source_fiscal': datetime.date(2017, 1, 1),
    }]
