import datetime

import pytest

import cepan

# Tuples corresponding to mock responses, expected shape of data frame.
return_value_testdata = [
    # Normal Response
    (
        [
            {
                "GroupDefinitions": [],
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
                "GroupDefinitions": [],
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
                "GroupDefinitions": [],
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
    df = cepan.get_cost_and_usage("", [], datetime.datetime(2020, 1, 1))
    assert df.shape == expected_shape
