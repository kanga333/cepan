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
    group_by_dimensions: Optional[List[str]] = None,
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
        "GroupBy": _build_group_by(group_by_dimensions),
    }
    response: Dict[str, Any] = client.get_cost_and_usage(**args)
    pre_df: List[Dict[str, str]] = []
    group_definitions: List[str] = []
    for definition in response["GroupDefinitions"]:
        group_definitions.append(definition["Key"])
    for row in response["ResultsByTime"]:
        time: str = row["TimePeriod"]["Start"]
        if row["Total"]:
            pre_row = _build_total_record(time, row)
            pre_df.append(pre_row)
        for group in row["Groups"]:
            pre_row = _build_group_record(time, group, group_definitions)
            pre_df.append(pre_row)
    return pd.DataFrame(pre_df, dtype="string")


def _build_group_by(
    group_by_dimensions: Optional[List[str]],
) -> List[Dict[str, str]]:
    group_by: List[Dict[str, str]] = []
    if group_by_dimensions:
        for val in group_by_dimensions:
            group_by.append({"Type": "DIMENSION", "Key": val})
    return group_by


def _build_total_record(time: str, row: Dict[str, Any]) -> Dict[str, str]:
    pre_row: Dict[str, str] = {"Time": time}
    for key, val in row["Total"].items():
        pre_row[key] = val["Amount"]
    return pre_row


def _build_group_record(
    time: str, group: Dict[str, Any], group_definitions: List[str]
) -> Dict[str, str]:
    pre_row: Dict[str, str] = {"Time": time}
    for definition, val in zip(group_definitions, group["Keys"]):
        pre_row[definition] = val
    for key, val in group["Metrics"].items():
        pre_row[key] = val["Amount"]
    return pre_row
