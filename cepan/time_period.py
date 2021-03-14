import datetime
from dataclasses import dataclass
from typing import Dict

_date_format = "%Y-%m-%d"
_time_format = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class TimePeriod:
    start: datetime.datetime
    end: datetime.datetime = datetime.datetime.now()

    def build(self, is_hourly: bool = False) -> Dict[str, str]:
        format = _time_format if is_hourly else _date_format
        return {
            "Start": self.start.strftime(format),
            "End": self.end.strftime(format),
        }
