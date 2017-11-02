import pandas
from tribble.transformers import clear_blanks
from tribble.transformers import contract_date_cleaner
from tribble.transformers import date_parser
from tribble.transformers import fiscal_date_converter
from tribble.transformers import reporting_periodizer
from tribble.transformers import schema_conformer


def transform(df: pandas.DataFrame) -> pandas.DataFrame:
    return (
        df.pipe(schema_conformer.SchemaConformer().apply)
        .pipe(date_parser.DateParser().apply)
        .pipe(fiscal_date_converter.FiscalDateConverter().apply)
        .pipe(contract_date_cleaner.ContractDateCleaner().apply)
        .pipe(clear_blanks.ClearBlanks().apply)
        .pipe(reporting_periodizer.ReportingPeriodizer().apply)
    )
