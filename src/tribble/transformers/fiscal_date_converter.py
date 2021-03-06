import datetime
import re
import typing
from dateutil import relativedelta
import pandas as pd
from tribble.transformers import base

_FISCAL_DATE_COLUMN = 'source_fiscal'


class FiscalDateConverter(base.BaseTransform):
    """Converts 'fiscal date' values to valid date values representing the beginning of the quarter.

    e.g. 201213-Q4 becomes 2013-01-01
    Values that can't be properly interpreted are converted to `None`."""

    _PATTERN = r'^([\d]{4})([\d]{2})-Q(\d)'

    def __init__(self, fiscal_date_column: typing.Optional[str] = None) -> None:
        self._fiscal_date_column = fiscal_date_column or _FISCAL_DATE_COLUMN

    @classmethod
    def _convert_date(cls, data: str) -> typing.Optional[datetime.date]:
        match = re.match(cls._PATTERN, data)
        if not match:
            return None

        start_year, end_year, quarter = int(match.group(1)), int(match.group(2)), int(match.group(3))
        end_year = end_year + 2000
        if end_year != start_year + 1:
            return None

        if not 1 <= quarter <= 4:
            return None

        if not 2000 < start_year < 2020:
            return None

        return datetime.date(start_year, 1, 1) + relativedelta.relativedelta(months=(3 * quarter))

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data[self._fiscal_date_column] = data[self._fiscal_date_column].apply(self._convert_date)
        return data


class BlankFiscalDateFilter(base.BaseTransform):
    """Removes rows with blank (null) `fiscal date` values."""

    def __init__(self, fiscal_date_column: typing.Optional[str] = None) -> None:
        self._fiscal_date_column = fiscal_date_column or _FISCAL_DATE_COLUMN

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.dropna(axis=0, subset=[self._fiscal_date_column])
