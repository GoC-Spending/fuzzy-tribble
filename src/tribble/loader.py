import pandas
from tribble import contract


def load_dataframe(df: pandas.DataFrame, model: contract.Base) -> None:
    data = df.to_dict('records')

    session = contract.Session()
    session.bulk_insert_mappings(model, data)
    session.commit()
