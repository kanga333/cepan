import datetime

import cepan


def test_get_dimensions(mocker):
    client_mock = mocker.Mock()
    client_mock.get_dimension_values.return_value = {
        "DimensionValues": [
            {"Value": "", "Attributes": {}},
            {"Value": "ap-northeast-1", "Attributes": {}},
        ],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    start = datetime.date(2020, 1, 1)
    df = cepan.get_dimension_values("AZ", start)
    assert len(df.index) == 1
    assert len(df.columns) == 2