import pandas as pd

from tribble.transformers import vendor_name_normalizer


def test_upcase() -> None:
    data = pd.DataFrame([
        {'id': 1, 'vendor_name': 'IBM Canada'}
    ])
    output = vendor_name_normalizer.VendorNameNormalizer().apply(data)
    assert output.to_dict('records') == [{'id': 1, 'vendor_name': 'IBM CANADA'}]


def test_punctuation_removal() -> None:
    data = pd.DataFrame([
        {'id': 1, 'vendor_name': 'I.B.M., CANADA?'}
    ])
    output = vendor_name_normalizer.VendorNameNormalizer().apply(data)
    assert output.to_dict('records') == [{'id': 1, 'vendor_name': 'IBM CANADA'}]


def test_organization_designation_removal() -> None:
    data = pd.DataFrame([
        {'id': 1, 'vendor_name': 'IBM CANADA LTD'},
        {'id': 2, 'vendor_name': 'NISHA TECHNOLOGIES INC.'},
        {'id': 3, 'vendor_name': 'SHRED-IT INTERNATIONAL ULC'},
        {'id': 4, 'vendor_name': 'D & D OILFIELD RENTALS CORP'},
        {'id': 5, 'vendor_name': 'DELOITTE & TOUCHE LLP'},
        {'id': 6, 'vendor_name': ' INCO CORP'}
    ])
    output = vendor_name_normalizer.VendorNameNormalizer().apply(data)
    assert sorted(output.to_dict('records'), key=lambda row: row['id']) == [
        {'id': 1, 'vendor_name': 'IBM CANADA'},
        {'id': 2, 'vendor_name': 'NISHA TECHNOLOGIES'},
        {'id': 3, 'vendor_name': 'SHREDIT INTERNATIONAL'},
        {'id': 4, 'vendor_name': 'D D OILFIELD RENTALS'},
        {'id': 5, 'vendor_name': 'DELOITTE TOUCHE'},
        {'id': 6, 'vendor_name': 'INCO'}
    ]


def test_whitespace_cleanup() -> None:
    data = pd.DataFrame([
        {'id': 1, 'vendor_name': '        IBM            CANADA          '}
    ])
    output = vendor_name_normalizer.VendorNameNormalizer().apply(data)
    assert output.to_dict('records') == [{'id': 1, 'vendor_name': 'IBM CANADA'}]
