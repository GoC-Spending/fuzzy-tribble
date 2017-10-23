import datetime
import itertools
import json
import os
import re
import typing
import pandas


def transform_dir(input_dir: str, grouping_length: int = 100) -> pandas.DataFrame:
    df: typing.Optional[pandas.DataFrame] = None

    blobs = _json_blobs(input_dir)
    for group in _grouper(blobs, grouping_length):
        chunk = [x for x in group if x]
        df = pandas.DataFrame(chunk) if df is None else df.append(chunk)

    return transform(df) if df is not None else pandas.DataFrame()


T = typing.TypeVar('T')


def _grouper(iterable: typing.Iterable[T], group_length: int) -> typing.Iterable[T]:
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * group_length
    return itertools.zip_longest(*args, fillvalue=None)


def _json_blobs(input_dir: str) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    input_filenames = [os.path.join(input_dir, dir_name) for dir_name in os.listdir(input_dir)]

    for filename in input_filenames:
        with open(filename) as input_file:
            yield json.loads(input_file.read())


def transform(df: pandas.DataFrame) -> pandas.DataFrame:
    return (
        df.pipe(conform_schema)
        .pipe(parse_dates)
    )


def conform_schema(df: pandas.DataFrame) -> pandas.DataFrame:
    column_renames = {
        'vendorName': 'vendor_name',
        'referenceNumber': 'reference_number',
        'contractDate': 'contract_date',
        'contractPeriodStart': 'contract_period_start',
        'contractPeriodEnd': 'contract_period_end',
        'deliveryDate': 'delivery_date',
        'contractValue': 'contract_value',
        'ownerAcronym': 'department',
        'sourceFiscal': 'source_fiscal',
        'uuid': 'uuid'
    }

    columns_to_drop = set(df.columns).difference(set(column_renames.keys()))

    return df.rename(columns=column_renames).drop(columns_to_drop, axis=1)


DATE_REGEX = re.compile(r'^([\d]{4})[\D]+([\d]{2})[\D]+([\d]{2})')


def parse_date(data: str) -> typing.Optional[datetime.date]:
    match = re.match(DATE_REGEX, data)
    if not match:
        return None

    try:
        year, month, day = int(match[1]), int(match[2]), int(match[3])
        if month > 12 and day <= 12:
            month, day = day, month
        parsed_date = datetime.date(year, month, day)
    except ValueError:
        return None

    return parsed_date if match else None


def parse_dates(df: pandas.DataFrame) -> pandas.DataFrame:
    for field_name in ('contract_date', 'contract_period_start', 'contract_period_end', 'delivery_date'):
        df[field_name] = df[field_name].apply(parse_date)
    return df
