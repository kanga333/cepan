import datetime

import pytest

import cepan as ce
from cepan import exceptions
from cepan._dimension import (
    _COST_AND_USAGE_DIMENSIONS,
    _RESERVATIONS_DIMENSIONS,
    _SAVINGS_PLANS_DIMENSIONS,
)
from cepan._filter import Dimensions
from cepan._sort_by import SortBy
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


@pytest.mark.parametrize(
    "func_args,expected_client_args",
    [
        # Request by Class
        (
            {
                "time_period": TimePeriod(
                    datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 2)
                ),
                "dimension": "REGION",
                "search_string": "ap",
                "context": "COST_AND_USAGE",
                "filter": Dimensions("REGION", ["ap-northeast-1"]),
                "sort_by": [SortBy("BlendedCost"), SortBy("UnblendedCost")],
                "max_results": 100,
            },
            {
                "TimePeriod": {
                    "Start": "2020-01-01",
                    "End": "2020-01-02",
                },
                "Dimension": "REGION",
                "SearchString": "ap",
                "Context": "COST_AND_USAGE",
                "Filter": {
                    "Dimensions": {
                        "Key": "REGION",
                        "Values": ["ap-northeast-1"],
                    },
                },
                "SortBy": [{"Key": "BlendedCost"}, {"Key": "UnblendedCost"}],
                "MaxResults": 100,
            },
        ),
    ],
)
def test_get_dimensions_args(mocker, func_args, expected_client_args):
    client_mock = mocker.Mock()
    client_mock.get_dimension_values.return_value = {
        "DimensionValues": [],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    ce.get_dimension_values(**func_args)
    kwargs = client_mock.get_dimension_values.call_args.kwargs
    assert kwargs == expected_client_args


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
        TimePeriod(start=datetime.datetime(2020, 1, 1)),
        "REGION",
    )
    assert len(df.index) == 1
    assert len(df.columns) == 2
