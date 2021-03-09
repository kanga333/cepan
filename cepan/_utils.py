import datetime
from typing import Any, Callable, Dict, Iterator, Optional

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


def call_with_pagination(
    client: boto3.client,
    func_name: str,
    args: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    func: Callable[..., Dict[str, Any]] = getattr(client, func_name)
    response: Dict[str, Any] = func(**args)
    yield response
    while "NextToken" in response:
        args["NextToken"] = response["NextToken"]
        response = func(**args)
        yield response
