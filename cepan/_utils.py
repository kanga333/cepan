from typing import Optional

import boto3


def client(
    service: str,
    session: Optional[boto3.Session] = None,
) -> boto3.client:
    if session is None:
        return boto3.client(service)

    return session.client(service)
