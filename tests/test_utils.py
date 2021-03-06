import datetime

from cepan._utils import build_date_period


def test_build_date_period():
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 1, 2)
    assert build_date_period(start, end) == {
        "Start": "2020-01-01",
        "End": "2020-01-02",
    }
