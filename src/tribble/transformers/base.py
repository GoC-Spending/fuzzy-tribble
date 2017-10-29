import abc
import pandas as pd


class BaseTransform(metaclass=abc.ABCMeta):

    def apply(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
