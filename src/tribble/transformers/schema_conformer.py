import typing
import pandas as pd
from tribble.transformers import base


class SchemaConformer(base.BaseTransform):

    def __init__(self, renames: typing.Optional[typing.Dict[str, str]] = None) -> None:
        self._renames = renames or self.COLUMN_RENAMES

    COLUMN_RENAMES = {
        'vendorName': 'vendor_name',
        'referenceNumber': 'reference_number',
        'contractDate': 'contract_date',
        'contractPeriodStart': 'contract_period_start',
        'contractPeriodEnd': 'contract_period_end',
        'deliveryDate': 'delivery_date',
        'contractValue': 'contract_value',
        'ownerAcronym': 'department',
        'sourceFiscal': 'source_fiscal',
        'uuid': 'uuid',
        'objectCode': 'object_code',
    }

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = set(data.columns).difference(set(self._renames.keys()))

        return data.rename(columns=self._renames).drop(columns_to_drop, axis=1)
