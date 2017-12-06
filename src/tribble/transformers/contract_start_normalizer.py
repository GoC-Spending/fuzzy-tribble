import pandas as pd
import numpy as np
from tribble.transformers import base


class ContractStartNormalizer(base.BaseTransform):
    """Sets all contract start dates for rows with matching `uuid` values to the minimum start date for that value.

    Handles contracts with start dates that are retroactively moved earlier."""
    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data['contract_period_start'] = np.min(data['contract_period_start'])
        return data
