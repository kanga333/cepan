import datetime
from typing import Any, Dict, List, Optional

import boto3
import pandas as pd

from cepan import _utils, exceptions


def get_cost_and_usage(
    granularity: str,
    metrics: List[str],
    start: datetime.datetime,
    end: datetime.datetime = datetime.datetime.now(),
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    client: boto3.client = _utils.client("ce", session)
    if granularity == "HOURLY":
        raise exceptions.UnsupportedGranularity(
            "Hourly granularity is not yet supported"
        )
    args: Dict[str, Any] = {
        "TimePeriod": _utils.build_date_period(start, end),
        "Granularity": granularity,
        "Metrics": metrics,
    }
    response: Dict[str, Any] = client.get_cost_and_usage(**args)
    pre_df: List[Dict[str, str]] = []
    for row in response["ResultsByTime"]:
        pre_row: Dict[str, str] = {"Time": row["TimePeriod"]["Start"]}
        for key, val in row["Total"].items():
            pre_row[key] = val["Amount"]
        pre_df.append(pre_row)
    return pd.DataFrame(pre_df, dtype="string")
