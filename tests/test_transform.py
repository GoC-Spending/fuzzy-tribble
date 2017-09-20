import json
import typing
import py._path.local
from tribble import transform


def data_template(overrides: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    data = {
        "uuid": "tbs-0000000000",
        "vendorName": "ABC Company",
        "referenceNumber": "0000000000",
        "contractDate": "2012-03-31",
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
    }
    data.update(overrides)
    return data


def test_transform_dir(tmpdir: py._path.local.LocalPath) -> None:
    data1_file = tmpdir.join('data1.json')
    data1 = data_template({
        "uuid": "tbs-0000000000",
        "vendorName": "ABC Company",
        "referenceNumber": "0000000000",
    })
    data1_file.write(json.dumps(data1))

    data2_file = tmpdir.join('data2.json')
    data2 = {
        "uuid": "tbs-0000000001",
        "vendorName": "XYZ Company",
        "referenceNumber": "0000000001",
    }
    data2_file.write(json.dumps(data2))

    output = transform.transform_dir(str(tmpdir))
    assert len(output) == 2


def test_chunking(tmpdir: py._path.local.LocalPath) -> None:
    for i in range(0, 100):
        data = data_template({'uuid': 'tbs-{}'.format(i)})
        data_file = tmpdir.join('data{}.json'.format(i))
        data_file.write(json.dumps(data))

    output = transform.transform_dir(str(tmpdir), grouping_length=7)
    assert len(output) == 100


def test_blank_dir(tmpdir: py._path.local.LocalPath) -> None:
    output = transform.transform_dir(str(tmpdir))
    assert len(output) == 0  # pylint: disable=len-as-condition
