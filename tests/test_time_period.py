import datetime

import pytest

from cepan.time_period import TimePeriod


@pytest.mark.parametrize(
    "args,is_hourly,expected",
    [
        (
            {
                "start": datetime.datetime(2020, 1, 1),
                "end": datetime.datetime(2020, 1, 2),
            },
            False,
            {"Start": "2020-01-01", "End": "2020-01-02"},
        ),
        (
            {
                "start": datetime.datetime(2020, 1, 1, 1),
                "end": datetime.datetime(2020, 1, 1, 2),
            },
            True,
            {"Start": "2020-01-01T01:00:00Z", "End": "2020-01-01T02:00:00Z"},
        ),
    ],
)
def test_time_period(args, is_hourly, expected):
    t = TimePeriod(**args)
    assert t.build(is_hourly) == expected
