import datetime

import pytest

import cepan as ce
from cepan._filter import Dimensions
from cepan._group_by import GroupBy
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
                "granularity": "DAILY",
                "metrics": ["AmortizedCost"],
                "filter": Dimensions("REGION", ["ap-northeast-1"]),
                "group_by": GroupBy(["AZ", "REGION"]),
            },
            {
                "TimePeriod": {
                    "Start": "2020-01-01",
                    "End": "2020-01-02",
                },
                "Granularity": "DAILY",
                "Filter": {
                    "Dimensions": {
                        "Key": "REGION",
                        "Values": ["ap-northeast-1"],
                    },
                },
                "Metrics": ["AmortizedCost"],
                "GroupBy": [
                    {"Type": "DIMENSION", "Key": "AZ"},
                    {"Type": "DIMENSION", "Key": "REGION"},
                ],
            },
        ),
        # # Request by Dict
        (
            {
                "time_period": {
                    "Start": "2020-01-01",
                    "End": "2020-01-02",
                },
                "granularity": "DAILY",
                "filter": {
                    "Dimensions": {
                        "Key": "REGION",
                        "Values": ["ap-northeast-1"],
                    },
                },
                "metrics": ["AmortizedCost"],
                "group_by": [
                    {"Type": "DIMENSION", "Key": "AZ"},
                    {"Type": "DIMENSION", "Key": "REGION"},
                ],
            },
            {
                "TimePeriod": {
                    "Start": "2020-01-01",
                    "End": "2020-01-02",
                },
                "Granularity": "DAILY",
                "Filter": {
                    "Dimensions": {
                        "Key": "REGION",
                        "Values": ["ap-northeast-1"],
                    },
                },
                "Metrics": ["AmortizedCost"],
                "GroupBy": [
                    {"Type": "DIMENSION", "Key": "AZ"},
                    {"Type": "DIMENSION", "Key": "REGION"},
                ],
            },
        ),
    ],
)
def test_get_cost_and_usage_args(mocker, func_args, expected_client_args):
    # Test that the response from the boto3.client can be converted to a Dataframe.
    client_mock = mocker.Mock()
    client_mock.get_cost_and_usage.return_value = {
        "ResultsByTime": [],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    ce.get_cost_and_usage(**func_args)
    kwargs = client_mock.get_cost_and_usage.call_args.kwargs
    assert kwargs == expected_client_args


# Tuples corresponding to mock responses, expected shape of data frame.
return_value_testdata = [
    # Normal Response
    (
        [
            {
                "ResultsByTime": [
                    {
                        "TimePeriod": {"Start": "2020-01-01", "End": "2020-01-02"},
                        "Total": {
                            "AmortizedCost": {"Amount": "1.0", "Unit": "USD"},
                            "BlendedCost": {"Amount": "1.1", "Unit": "USD"},
                        },
                        "Groups": [],
                        "Estimated": False,
                    },
                    {
                        "TimePeriod": {"Start": "2020-01-02", "End": "2020-01-03"},
                        "Total": {
                            "AmortizedCost": {"Amount": "2.0", "Unit": "USD"},
                            "BlendedCost": {"Amount": "2.1", "Unit": "USD"},
                        },
                        "Groups": [],
                        "Estimated": False,
                    },
                ],
            }
        ],
        (2, 3),
    ),
    # GroupBy Response
    (
        [
            {
                "GroupDefinitions": [
                    {"Type": "DIMENSION", "Key": "REGION"},
                    {"Type": "DIMENSION", "Key": "AZ"},
                ],
                "ResultsByTime": [
                    {
                        "TimePeriod": {"Start": "2020-01-01", "End": "2020-01-02"},
                        "Total": {},
                        "Groups": [
                            {
                                "Keys": ["NoRegion", "NoAZ"],
                                "Metrics": {
                                    "AmortizedCost": {
                                        "Amount": "0.001",
                                        "Unit": "USD",
                                    },
                                    "BlendedCost": {
                                        "Amount": "0.002",
                                        "Unit": "USD",
                                    },
                                },
                            },
                            {
                                "Keys": ["ap-northeast-1", "NoAZ"],
                                "Metrics": {
                                    "AmortizedCost": {
                                        "Amount": "0.003",
                                        "Unit": "USD",
                                    },
                                    "BlendedCost": {
                                        "Amount": "0.004",
                                        "Unit": "USD",
                                    },
                                },
                            },
                        ],
                        "Estimated": False,
                    },
                    {
                        "TimePeriod": {"Start": "2020-01-02", "End": "2020-01-03"},
                        "Total": {},
                        "Groups": [
                            {
                                "Keys": ["NoRegion", "NoAZ"],
                                "Metrics": {
                                    "AmortizedCost": {
                                        "Amount": "0.005",
                                        "Unit": "USD",
                                    },
                                    "BlendedCost": {
                                        "Amount": "0.006",
                                        "Unit": "USD",
                                    },
                                },
                            },
                            {
                                "Keys": ["ap-northeast-1", "NoAZ"],
                                "Metrics": {
                                    "AmortizedCost": {
                                        "Amount": "0.007",
                                        "Unit": "USD",
                                    },
                                    "BlendedCost": {
                                        "Amount": "0.008",
                                        "Unit": "USD",
                                    },
                                },
                            },
                        ],
                        "Estimated": False,
                    },
                ],
            }
        ],
        (4, 5),
    ),
    # Pagination Response
    (
        [
            {
                "NextPageToken": "Next",
                "ResultsByTime": [
                    {
                        "TimePeriod": {"Start": "2020-01-01", "End": "2020-01-02"},
                        "Total": {
                            "AmortizedCost": {"Amount": "1.0", "Unit": "USD"},
                        },
                        "Groups": [],
                        "Estimated": False,
                    }
                ],
            },
            {
                "ResultsByTime": [
                    {
                        "TimePeriod": {"Start": "2020-01-02", "End": "2020-01-03"},
                        "Total": {
                            "AmortizedCost": {"Amount": "2.0", "Unit": "USD"},
                        },
                        "Groups": [],
                        "Estimated": False,
                    },
                ],
            },
        ],
        (2, 2),
    ),
]


@pytest.mark.parametrize(
    "mock_response,expected_shape",
    return_value_testdata,
)
def test_get_cost_and_usage_return_value(mocker, mock_response, expected_shape):
    # Test that the response from the boto3.client can be converted to a Dataframe.
    client_mock = mocker.Mock()
    client_mock.get_cost_and_usage.side_effect = mock_response
    mocker.patch("boto3.client", return_value=client_mock)
    df = ce.get_cost_and_usage(TimePeriod(datetime.datetime(2020, 1, 1)), "")
    assert df.shape == expected_shape


@pytest.mark.parametrize(
    "dtype",
    ["float64", "string"],
)
def test_get_cost_and_usage_dtype(mocker, dtype):
    # Test that the dtype of the metrics column is set correctly.
    client_mock = mocker.Mock()
    client_mock.get_cost_and_usage.return_value = {
        "ResultsByTime": [
            {
                "TimePeriod": {"Start": "2020-01-01", "End": "2020-01-02"},
                "Total": {
                    "AmortizedCost": {"Amount": "1.0", "Unit": "USD"},
                },
                "Groups": [],
                "Estimated": False,
            }
        ],
    }
    mocker.patch("boto3.client", return_value=client_mock)
    df = ce.get_cost_and_usage(
        TimePeriod(datetime.datetime(2020, 1, 1)), "", metrics_dtype=dtype
    )
    assert df["AmortizedCost"].dtype == dtype
