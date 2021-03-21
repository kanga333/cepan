import datetime
from dataclasses import dataclass
from typing import Dict, Union

_date_format = "%Y-%m-%d"
_time_format = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class TimePeriod:
    """The time period of the request.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_DateInterval.html
    """

    start: datetime.datetime
    end: datetime.datetime = datetime.datetime.now()

    def build(self, is_hourly: bool = False) -> Dict[str, str]:
        format = _time_format if is_hourly else _date_format
        return {
            "Start": self.start.strftime(format),
            "End": self.end.strftime(format),
        }


def _build_time_period(
    time_period: Union[TimePeriod, Dict[str, str]], is_hourly: bool = False
) -> Dict[str, str]:
    if isinstance(time_period, Dict):
        return time_period
    return time_period.build()
