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
            pre_df.append(_process_total_row(time, row["Total"]))
        for group in row["Groups"]:
            pre_df.append(_process_group_row(time, group, group_definitions))
    return pd.DataFrame(pre_df, dtype="string")


def _build_group_by(
    group_by_dimensions: Optional[List[str]],
) -> List[Dict[str, str]]:
    group_by: List[Dict[str, str]] = []
    if group_by_dimensions:
        for val in group_by_dimensions:
            group_by.append({"Type": "DIMENSION", "Key": val})
    return group_by


def _process_total_row(time: str, total_row: Dict[str, Any]) -> Dict[str, str]:
    processed: Dict[str, str] = {"Time": time}
    for key, val in total_row.items():
        processed[key] = val["Amount"]
    return processed


def _process_group_row(
    time: str, group_row: Dict[str, Any], group_definitions: List[str]
) -> Dict[str, str]:
    processed: Dict[str, str] = {"Time": time}
    for definition, val in zip(group_definitions, group_row["Keys"]):
        processed[definition] = val
    for key, val in group_row["Metrics"].items():
        processed[key] = val["Amount"]
    return processed
