import datetime
import pandas as pd
import numpy as np
from tribble.transformers import base


class ReportingPeriodizer(base.BaseTransform):
    """Breaks up each row for a single `uuid` value into non-overlapping reporting period values."""

    MAX_DATE = datetime.date(9999, 12, 31)

    @staticmethod
    def _least(*columns: pd.Series) -> pd.Series:
        least = None
        for column in columns:
            least = column if least is None else np.where(column < least, column, least)
        assert least is not None
        return least

    @staticmethod
    def _greatest(*columns: pd.Series) -> pd.Series:
        greatest = None
        for column in columns:
            greatest = column if greatest is None else np.where(column > greatest, column, greatest)
        assert greatest is not None
        return greatest

    @classmethod
    def _period_starts(cls,
                       source_fiscal: pd.Series,
                       contract_date: pd.Series,
                       contract_period_start: pd.Series,
                       contract_period_end: pd.Series) -> pd.Series:
        prior_contract_period_end = contract_period_end.shift(1)

        return np.where(pd.isnull(prior_contract_period_end),
                        contract_period_start,
                        cls._greatest(source_fiscal, contract_period_start, contract_date))

    @classmethod
    def _period_ends(cls, period_start: pd.Series, contract_period_end: pd.Series) -> pd.Series:
        next_period_start = period_start.shift(-1)

        return np.where(pd.isnull(next_period_start),
                        contract_period_end,
                        next_period_start - datetime.timedelta(days=1))

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.sort_values(['source_fiscal', 'contract_date'])
        data['reporting_period_start'] = self._period_starts(data['source_fiscal'],
                                                             data['contract_date'],
                                                             data['contract_period_start'],
                                                             data['contract_period_end'])
        data['reporting_period_end'] = self._period_ends(data['reporting_period_start'], data['contract_period_end'])
        return data
