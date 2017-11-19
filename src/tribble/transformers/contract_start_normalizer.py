import pandas as pd
import numpy as np
from tribble.transformers import base


class ContractStartNormalizer(base.BaseTransform):
    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        data['contract_period_start'] = np.min(data['contract_period_start'])
        return data
