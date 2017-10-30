import datetime
import pandas as pd
from tribble.transformers import base


class ReportingPeriodizer(base.BaseTransform):

    MAX_DATE = datetime.date(9999, 12, 31)

    @staticmethod
    def _period_ends(row: pd.Series) -> pd.Series:
        if row['next_source_fiscal'] and not pd.isnull(row['next_source_fiscal']):
            day_before_next_fiscal = row['next_source_fiscal'] - datetime.timedelta(days=1)
            end = min(row['contract_period_end'], day_before_next_fiscal)
        else:
            end = row['contract_period_end']
        row['reporting_period_end'] = end
        return row

    @classmethod
    def _period_starts(cls, row: pd.Series) -> pd.Series:
        if row['last_contract_period_end']  and not pd.isnull(row['last_contract_period_end']):
            day_after_last_end = row['last_contract_period_end'] + datetime.timedelta(days=1)
            start = min(row['source_fiscal'] or cls.MAX_DATE, day_after_last_end)
        else:
            start = min(row['contract_period_start'], row['source_fiscal'] or cls.MAX_DATE)
        row['reporting_period_start'] = start
        return row

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.sort_values(['uuid', 'contract_period_start', 'source_fiscal'])
        grouped_data = data.groupby('uuid', sort=False)
        data['next_source_fiscal'] = grouped_data['source_fiscal'].shift(-1)
        data['last_contract_period_end'] = grouped_data['contract_period_end'].shift(1)

        return data.apply(self._period_ends, reduce=False, axis=1) \
            .apply(self._period_starts, reduce=False, axis=1) \
            .drop(['next_source_fiscal', 'last_contract_period_end'], axis=1)
