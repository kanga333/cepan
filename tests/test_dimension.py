import datetime

import cepan as ce
from cepan._time_period import TimePeriod


def test_get_dimensions(mocker):
    client_mock = mocker.Mock()
    client_mock.get_dimension_values.return_value = {
        "DimensionValues": [
            {"Value": "", "Attributes": {}},
            {"Value": "ap-northeast-1", "Attributes": {}},
        ],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    df = ce.get_dimension_values(
        "AZ",
        TimePeriod(start=datetime.datetime(2020, 1, 1)),
    )
    assert len(df.index) == 1
    assert len(df.columns) == 2
