import pandas
import pytest
from tribble import loader


@pytest.mark.usefixtures('db')
def test_load_dataframe() -> None:
    df = pandas.DataFrame([
        {'uuid': 'foo'},
        {'uuid': 'bar'},
    ])

    loader.load_dataframe(df)
