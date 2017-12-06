import pandas as pd
from tribble.transformers import base


class ClearBlanks(base.BaseTransform):
    """Replaces empty values in the specified or default fields with `None`."""

    FIELDS_TO_CLEAR = ['object_code']

    def __init__(self, *fields: str) -> None:
        self._fields = fields or self.FIELDS_TO_CLEAR

    @staticmethod
    def _clear_blank(data):
        return data if data else None

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        for field_name in self._fields:
            data[field_name] = data[field_name].apply(self._clear_blank)
        return data
