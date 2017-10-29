import datetime
import re
import typing
import pandas as pd
from tribble.transformers import base


class DateParser(base.BaseTransform):

    def __init__(self, *fields: str) -> None:
        self._fields = fields or self._FIELDS

    _FIELDS = ['contract_date', 'contract_period_start', 'contract_period_end', 'delivery_date']
    _DATE_REGEX = re.compile(r'^([\d]{4})[\D]+([\d]{2})[\D]+([\d]{2})')

    @classmethod
    def _parse_date(cls, data: str) -> typing.Optional[datetime.date]:
        match = re.match(cls._DATE_REGEX, data)
        if not match:
            return None

        try:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            if month > 12 and day <= 12:
                month, day = day, month
            parsed_date = datetime.date(year, month, day)
        except ValueError:
            return None

        return parsed_date if match else None

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        for field_name in self._fields:
            data[field_name] = data[field_name].apply(self._parse_date)
        return data
