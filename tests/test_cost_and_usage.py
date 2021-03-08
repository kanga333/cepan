import datetime

import pytest

import cepan

# Tuples corresponding to
# mock response, expected number of lines and expected number of rows.
testdata = [
    (
        {
            "GroupDefinitions": [],
            "ResultsByTime": [
                {
                    "TimePeriod": {"Start": "2021-01-01", "End": "2021-02-01"},
                    "Total": {
                        "AmortizedCost": {"Amount": "1.0", "Unit": "USD"},
                        "BlendedCost": {"Amount": "1.1", "Unit": "USD"},
                    },
                    "Groups": [],
                    "Estimated": False,
                },
                {
                    "TimePeriod": {"Start": "2021-02-01", "End": "2021-02-04"},
                    "Total": {
                        "AmortizedCost": {"Amount": "2.0", "Unit": "USD"},
                        "BlendedCost": {"Amount": "2.1", "Unit": "USD"},
                    },
                    "Groups": [],
                    "Estimated": False,
                },
            ],
        },
        2,
        3,
    ),
    (
        {
            "GroupDefinitions": [
                {"Type": "DIMENSION", "Key": "REGION"},
                {"Type": "DIMENSION", "Key": "AZ"},
            ],
            "ResultsByTime": [
                {
                    "TimePeriod": {"Start": "2021-01-01", "End": "2021-01-02"},
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
                    "TimePeriod": {"Start": "2021-01-02", "End": "2021-01-03"},
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
        },
        4,
        5,
    ),
]


@pytest.mark.parametrize(
    "mock_response,expected_lines,expected_rows",
    testdata,
)
def test_get_cost_and_usage(
    mocker,
    mock_response,
    expected_lines,
    expected_rows,
):
    client_mock = mocker.Mock()
    client_mock.get_cost_and_usage.return_value = mock_response
    mocker.patch("boto3.client", return_value=client_mock)
    start = datetime.datetime(2020, 1, 1)
    df = cepan.get_cost_and_usage(
        "MONTHLY",
        ["AmortizedCost", "BlendedCost"],
        start,
    )
    assert len(df.index) == expected_lines
    assert len(df.columns) == expected_rows
