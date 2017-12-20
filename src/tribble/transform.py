import typing
import pandas
import pandas.core.groupby
from tribble.transformers import base
from tribble.transformers import clear_blanks
from tribble.transformers import contract_date_cleaner
from tribble.transformers import contract_start_normalizer
from tribble.transformers import date_parser
from tribble.transformers import fiscal_date_converter
from tribble.transformers import reporting_period_value
from tribble.transformers import reporting_periodizer
from tribble.transformers import schema_conformer
from tribble import log
from tribble.log import tqdm

tqdm.pandas()
LOGGER = log.get_logger(__name__)



TRANSFORMERS: typing.List[typing.Type[base.BaseTransform]] = [
    schema_conformer.SchemaConformer,
    date_parser.DateParser,
    fiscal_date_converter.FiscalDateConverter,
    fiscal_date_converter.BlankFiscalDateFilter,
    contract_date_cleaner.ContractDateCleaner,
    clear_blanks.ClearBlanks,
]


GROUP_TRANSFORMERS: typing.List[typing.Type[base.BaseTransform]] = [
    contract_start_normalizer.ContractStartNormalizer,
    reporting_periodizer.ReportingPeriodizer,
    reporting_period_value.ReportingPeriodValue,
]


def transform(df: pandas.DataFrame) -> pandas.DataFrame:
    LOGGER.info(f'Applying {len(TRANSFORMERS)} regular transformers:')
    df = _apply_transform_list(df, TRANSFORMERS, show_progress=True)
    uuid_grouped = df.groupby('uuid')
    LOGGER.info(f'Applying group transformers to {len(uuid_grouped)} uuids ' +
                f'(needs {len(uuid_grouped)+1} operations):')
    return df.groupby('uuid').progress_apply(_group_transform_df)


def _apply_transform_list(df: pandas.DataFrame,
                          transformer_classes: typing.List[typing.Type[base.BaseTransform]],
                          show_progress: bool = False
                         ) -> pandas.DataFrame:
    for transformer_class in transformer_classes if not show_progress else tqdm(transformer_classes):
        df = transformer_class().apply(df)
    return df


def _group_transform_df(df: pandas.DataFrame) -> pandas.DataFrame:
    df = df.sort_values(['contract_period_start', 'source_fiscal'])
    return _apply_transform_list(df, GROUP_TRANSFORMERS)
