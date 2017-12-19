import datetime
import typing
import numpy as np
import pandas as pd
from tribble.transformers import base


class ReportingPeriodValue(base.BaseTransform):

    @staticmethod
    def days_in_range(start: pd.Series, end: pd.Series) -> float:
        return (end - start + datetime.timedelta(days=1)) / np.timedelta64(1, 'D')  # pylint: disable=no-member

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        consumed_value = 0.0
        consumed_days = 0
        values: typing.List[float] = []
        indexes: typing.List[int] = []
        for index, row in data.iterrows():
            days_in_period = (
                row['reporting_period_end'] - row['reporting_period_start'] + datetime.timedelta(days=1)
            ).days
            days_in_contract = (
                row['contract_period_end'] - row['contract_period_start'] + datetime.timedelta(days=1)
            ).days
            remaining_value = row['contract_value'] - consumed_value
            reporting_period_value = np.round(remaining_value * days_in_period / (days_in_contract - consumed_days), 2)
            values.append(reporting_period_value)
            indexes.append(index)
            consumed_value += reporting_period_value
            consumed_days += days_in_period
        data = data.assign(reporting_period_value=pd.Series(data=values, index=indexes))
        return data
