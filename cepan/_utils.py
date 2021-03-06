import datetime
from typing import Dict, Optional

import boto3

_date_format = "%Y-%m-%d"


def client(
    service: str,
    session: Optional[boto3.Session] = None,
) -> boto3.client:
    if session is None:
        return boto3.client(service)

    return session.client(service)


def build_date_period(
    start: datetime.datetime,
    end: datetime.datetime,
) -> Dict[str, str]:
    return {
        "Start": start.strftime(_date_format),
        "End": end.strftime(_date_format),
    }
