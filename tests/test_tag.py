import datetime

import pytest

import cepan as ce
from cepan._filter import Dimensions
from cepan._sort_by import SortBy
from cepan._time_period import TimePeriod


@pytest.mark.parametrize(
    "func_args,expected_client_args",
    [
        # Request by Class
        (
            {
                "time_period": TimePeriod(
                    datetime.datetime(2020, 1, 1), datetime.datetime(2020, 1, 2)
                ),
                "tag_key": "key",
                "search_string": "ap",
                "filter": Dimensions("REGION", ["ap-northeast-1"]),
                "sort_by": [SortBy("BlendedCost"), SortBy("UnblendedCost")],
                "max_results": 100,
            },
            {
                "TimePeriod": {
                    "Start": "2020-01-01",
                    "End": "2020-01-02",
                },
                "TagKey": "key",
                "SearchString": "ap",
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
def test_get_tags_args(mocker, func_args, expected_client_args):
    client_mock = mocker.Mock()
    client_mock.get_tags.return_value = {
        "Tags": [],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    ce.get_tags(**func_args)
    kwargs = client_mock.get_tags.call_args.kwargs
    assert kwargs == expected_client_args


def test_get_tags(mocker):
    client_mock = mocker.Mock()
    client_mock.get_tags.return_value = {
        "Tags": ["", "A", "B", "C"],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    df = ce.get_tags(
        TimePeriod(start=datetime.datetime(2020, 1, 1)),
        "key",
    )
    assert len(df.index) == 3
    assert len(df.columns) == 2
