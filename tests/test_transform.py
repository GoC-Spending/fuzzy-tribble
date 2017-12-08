import datetime
import typing
import pandas
import pytest
from tribble import transform


class DataTemplate:

    def __init__(self, default: typing.Dict[str, typing.Any]) -> None:
        self._default = default

    def _generate_rows(self,
                       overrides: typing.List[typing.Dict[str, typing.Any]]
                      ) -> typing.Iterable[typing.Dict[str, typing.Any]]:
        for row in overrides:
            assert set(row.keys()).intersection(set(self._default.keys())) == set(row.keys())

            generated_row = self._default.copy()
            generated_row.update(row)
            yield generated_row

    def to_df(self, overrides: typing.List[typing.Dict[str, typing.Any]]) -> pandas.DataFrame:
        return pandas.DataFrame(self._generate_rows(overrides))

    def to_dicts(self,
                 overrides: typing.List[typing.Dict[str, typing.Any]]
                ) -> typing.List[typing.Dict[str, typing.Any]]:
        return list(self._generate_rows(overrides))


@pytest.fixture
def input_template() -> DataTemplate:
    return DataTemplate({
        "uuid": "tbs-0000000000",
        "vendorName": "ABC Company",
        "referenceNumber": "0000000000",
        "contractDate": "2012â03â31",
        "description": "499 OTHER PROFESSIONAL SERVICES NOT ELSEWHERE SPECIFIED",
        "extraDescription": "Big Contract #1",
        "objectCode": "0499",
        "contractPeriodStart": "2012-04-01",
        "contractPeriodEnd": "2018-03-31",
        "startYear": "2012",
        "endYear": "2018",
        "deliveryDate": "",
        "originalValue": 6000.0,
        "contractValue": 6000,
        "comments": "This contract includes one or more amendments.This contract was competitively sourced." +
                    "This contract is a multi-year contract.",
        "ownerAcronym": "tbs",
        "sourceYear": 2012,
        "sourceQuarter": 1,
        "sourceFiscal": "201213-Q4",
        "sourceFilename": r"tbs\/5ae78038dd512ae3f7e8a91349f443cb.html",
        "sourceURL": r"http:\/\/www.tbs-sct.gc.ca\/scripts\/contracts-contrats\/reports-rapports-eng.asp" +
                     "?r=c&refNum=0000000000&q=4&yr=2012&d=",
        "amendedValues": [],
        "contractPeriodRange": "2012-04-01 to 2018-03-31",
        "yearsDuration": 6,
        "valuePerYear": 1000.0,
        "vendorClean": "Big Contract #1"
    })


@pytest.fixture
def output_template() -> DataTemplate:
    return DataTemplate({
        "uuid": "tbs-0000000000",
        "vendor_name": "ABC Company",
        "reference_number": "0000000000",
        "contract_date": datetime.date(2012, 3, 31),
        "contract_period_start": datetime.date(2012, 4, 1),
        "contract_period_end": datetime.date(2018, 3, 31),
        "reporting_period_start": datetime.date(2012, 4, 1),
        "reporting_period_end": datetime.date(2018, 3, 31),
        "contract_value": 6000,
        "department": "tbs",
        "source_fiscal": datetime.date(2013, 1, 1),
        "object_code": "0499"
    })


def test_transform(input_template: DataTemplate, output_template: DataTemplate) -> None:
    data = input_template.to_df([{}])
    output = transform.transform(data).to_dict('records')
    expected = output_template.to_dicts([{}])
    assert output == expected


def test_fiscal_date_converter(input_template: DataTemplate, output_template: DataTemplate) -> None:
    data = input_template.to_df([
        {'uuid': '1', 'sourceFiscal': '201213-Q1'},
        {'uuid': '2', 'sourceFiscal': '201213-Q2'},
        {'uuid': '3', 'sourceFiscal': '201213-Q3'},
        {'uuid': '4', 'sourceFiscal': '201213-Q4'},
    ])
    output = transform.transform(data).to_dict('records')
    expected = output_template.to_dicts([
        {
            'uuid': '1',
            'source_fiscal': datetime.date(2012, 4, 1),
            'reporting_period_start': datetime.date(2012, 4, 1),
            'reporting_period_end': datetime.date(2018, 3, 31),
        }, {
            'uuid': '2',
            'source_fiscal': datetime.date(2012, 7, 1),
            'reporting_period_start': datetime.date(2012, 4, 1),
            'reporting_period_end': datetime.date(2018, 3, 31),
        }, {
            'uuid': '3',
            'source_fiscal': datetime.date(2012, 10, 1),
            'reporting_period_start': datetime.date(2012, 4, 1),
            'reporting_period_end': datetime.date(2018, 3, 31),
        }, {
            'uuid': '4',
            'source_fiscal': datetime.date(2013, 1, 1),
            'reporting_period_start': datetime.date(2012, 4, 1),
            'reporting_period_end': datetime.date(2018, 3, 31),
        },
    ])
    assert output == expected


def test_fiscal_date_converting_bad_data(input_template: DataTemplate) -> None:
    data = input_template.to_df([
        {'uuid': 1, 'sourceFiscal': '2012-04-01'},
        {'uuid': 2, 'sourceFiscal': '201213'},
        {'uuid': 3, 'sourceFiscal': '201213-Q5'},
    ])
    output = transform.transform(data).to_dict('records')
    assert output == []


def test_bad_contract_dates(input_template: DataTemplate, output_template: DataTemplate) -> None:
    data = input_template.to_df([{
        'contractDate': '2012-10-10',
        'contractPeriodStart': '0001-01-01',
        'contractPeriodEnd': '1899-12-31',
    }])

    expected = output_template.to_dicts([{
        'contract_date': datetime.date(2012, 10, 10),
        'contract_period_start': datetime.date(2012, 10, 10),
        'contract_period_end': datetime.date(2012, 10, 10),
        'reporting_period_start': datetime.date(2012, 10, 10),
        'reporting_period_end': datetime.date(2012, 10, 10),
    }])
    assert transform.transform(data).to_dict('records') == expected


def test_reporting_periods_broken_up(input_template: DataTemplate, output_template: DataTemplate) -> None:
    data = input_template.to_df([
        {
            'contractDate': '2012-10-02',
            'contractPeriodStart': '2012-10-01',
            'contractPeriodEnd': '2014-12-31',
            'sourceFiscal': '201213-Q3'
        }, {
            'contractDate': '2014-01-02',
            'contractPeriodStart': '2012-10-01',
            'contractPeriodEnd': '2015-12-31',
            'sourceFiscal': '201314-Q4'
        }
    ])

    expected = output_template.to_dicts([
        {
            'contract_date': datetime.date(2012, 10, 2),
            'contract_period_start': datetime.date(2012, 10, 1),
            'contract_period_end': datetime.date(2014, 12, 31),
            'source_fiscal': datetime.date(2012, 10, 1),
            'reporting_period_start': datetime.date(2012, 10, 1),
            'reporting_period_end': datetime.date(2013, 12, 31),
        }, {
            'contract_date': datetime.date(2014, 1, 2),
            'contract_period_start': datetime.date(2012, 10, 1),
            'contract_period_end': datetime.date(2015, 12, 31),
            'source_fiscal': datetime.date(2014, 1, 1),
            'reporting_period_start': datetime.date(2014, 1, 1),
            'reporting_period_end': datetime.date(2015, 12, 31),
        }
    ])

    assert transform.transform(data).to_dict('records') == expected


def test_contract_starts_that_go_backwards_in_time(input_template: DataTemplate, output_template: DataTemplate) -> None:
    data = input_template.to_df([
        {
            'contractDate': '2012-01-01',
            'contractPeriodStart': '2011-12-01',
            'contractPeriodEnd': '2014-01-01',
            'sourceFiscal': '201213-Q4',
        }, {
            'contractDate': '2013-01-01',
            'contractPeriodStart': '2010-01-01',
            'contractPeriodEnd': '2015-01-01',
            'sourceFiscal': '201314-Q1',
        }
    ])
    output = transform.transform(data).to_dict('records')
    output = sorted(output, key=lambda r: r['contract_date'])

    expected = output_template.to_dicts([
        {
            'contract_date': datetime.date(2012, 1, 1),
            'contract_period_start': datetime.date(2010, 1, 1),
            'contract_period_end': datetime.date(2014, 1, 1),
            'source_fiscal': datetime.date(2013, 1, 1),
            'reporting_period_start': datetime.date(2010, 1, 1),
            'reporting_period_end': datetime.date(2013, 3, 31),
        }, {
            'contract_date': datetime.date(2013, 1, 1),
            'contract_period_start': datetime.date(2010, 1, 1),
            'contract_period_end': datetime.date(2015, 1, 1),
            'source_fiscal': datetime.date(2013, 4, 1),
            'reporting_period_start': datetime.date(2013, 4, 1),
            'reporting_period_end': datetime.date(2015, 1, 1),
        }
    ])
    assert output == expected


def test_blank_fiscal_rows_dropped(input_template: DataTemplate) -> None:
    data = input_template.to_df([
        {'sourceFiscal': ''},
    ])

    output = transform.transform(data).to_dict('records')
    assert output == []
