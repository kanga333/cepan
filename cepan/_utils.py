from typing import Any, Callable, Dict, Iterator, Optional

import boto3


def client(
    service: str,
    session: Optional[boto3.Session] = None,
) -> boto3.client:
    if session is None:
        return boto3.client(service)

    return session.client(service)


def call_with_pagination(
    client: boto3.client,
    func_name: str,
    args: Dict[str, Any],
) -> Iterator[Dict[str, Any]]:
    func: Callable[..., Dict[str, Any]] = getattr(client, func_name)
    response: Dict[str, Any] = func(**args)
    yield response
    token_key: Optional[str] = None
    if "NextToken" in response:
        token_key = "NextToken"
    if "NextPageToken" in response:
        token_key = "NextPageToken"
    while token_key in response:
        args[token_key] = response[token_key]
        response = func(**args)
        yield response
