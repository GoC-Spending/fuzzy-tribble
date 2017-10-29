import pandas as pd
from tribble.transformers import base


class ContractDateCleaner(base.BaseTransform):

    @staticmethod
    def _set_null_contract_dates(row: pd.Series) -> pd.Series:
        if row['contract_date'] is None:
            row['contract_date'] = row['source_fiscal']
        return row

    @staticmethod
    def _clean_row(row: pd.Series) -> pd.Series:
        if row['contract_period_start'] is not None:
            if row['contract_period_end'] is None:
                row['contract_period_end'] = row['contract_period_start']
        elif row['delivery_date'] is not None:
            assert row['contract_period_end'] is None, \
                f'contract_period_end and delivery_date are both populated: #{row}'

            row['contract_period_start'] = row['delivery_date']
            row['contract_period_end'] = row['delivery_date']
        else:
            row['contract_period_start'] = row['contract_date']
            row['contract_period_end'] = (
                row['contract_period_end'] if row['contract_period_end'] else row['contract_date'])

        return row

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        cleaned = data.apply(self._set_null_contract_dates, reduce=False, axis=1) \
            .apply(self._clean_row, reduce=False, axis=1)
        return cleaned.drop(['delivery_date'], axis=1)
