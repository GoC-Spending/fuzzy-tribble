import pandas
from tribble import contract


def load_dataframe(df: pandas.DataFrame) -> None:
    data = df.to_dict('records')

    session = contract.Session()
    session.bulk_insert_mappings(contract.Contract, data)
    session.commit()
