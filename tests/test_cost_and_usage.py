import datetime

import cepan


def test_get_cost_and_usage(mocker):
    client_mock = mocker.Mock()
    client_mock.get_cost_and_usage.return_value = {
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
    }
    mocker.patch("boto3.client", return_value=client_mock)
    start = datetime.datetime(2020, 1, 1)
    df = cepan.get_cost_and_usage(
        "MONTHLY",
        ["AmortizedCost", "BlendedCost"],
        start,
    )
    assert len(df.index) == 2
    assert len(df.columns) == 3
