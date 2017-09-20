import itertools
import json
import os
import typing
import pandas


def transform_dir(input_dir: str, grouping_length: int = 100) -> pandas.DataFrame:
    df: typing.Optional[pandas.DataFrame] = None

    blobs = _json_blobs(input_dir)
    for group in _grouper(blobs, grouping_length):
        chunk = [x for x in group if x]
        df = pandas.DataFrame(chunk) if df is None else df.append(chunk)

    return df if df is not None else pandas.DataFrame()


T = typing.TypeVar('T')


def _grouper(iterable: typing.Iterable[T], group_length: int) -> typing.Iterable[T]:
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * group_length
    return itertools.zip_longest(*args, fillvalue=None)


def _json_blobs(input_dir: str) -> typing.Iterator[typing.Dict[str, typing.Any]]:
    input_filenames = [os.path.join(input_dir, dir_name) for dir_name in os.listdir(input_dir)]

    for filename in input_filenames:
        with open(filename) as input_file:
            yield json.loads(input_file.read())
