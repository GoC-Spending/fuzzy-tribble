import datetime
import typing
import pandas
import pytest
from tribble import contract
from tribble import loader


@pytest.mark.usefixtures('db')
def test_load_dataframe() -> None:
    contract_date = datetime.date(2017, 1, 1)
    row: typing.Dict[str, typing.Any] = {
        'contract_date': contract_date,
        'contract_period_start': contract_date,
        'contract_period_end': contract_date,
        'reporting_period_start': contract_date,
        'reporting_period_end': contract_date,
        'reporting_period_value': 1.00
    }
    row1 = row.copy()
    row1['uuid'] = 'foo'
    row2 = row.copy()
    row2['uuid'] = 'bar'
    data = [row1, row2]
    df = pandas.DataFrame(data)

    loader.load_dataframe(df, contract.Contract)
