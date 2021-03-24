import datetime

import pytest

import cepan as ce
from cepan import exceptions
from cepan._dimension import (
    _COST_AND_USAGE_DIMENSIONS,
    _RESERVATIONS_DIMENSIONS,
    _SAVINGS_PLANS_DIMENSIONS,
)
from cepan._time_period import TimePeriod


def test_show_dimensions(mocker):
    dimensions = ce.show_dimensions()
    assert dimensions == _COST_AND_USAGE_DIMENSIONS
    dimensions = ce.show_dimensions(context="RESERVATIONS")
    assert dimensions == _RESERVATIONS_DIMENSIONS
    dimensions = ce.show_dimensions(context="SAVINGS_PLANS")
    assert dimensions == _SAVINGS_PLANS_DIMENSIONS
    with pytest.raises(exceptions.InvalidParameter):
        ce.show_dimensions(context="Invalid")


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
