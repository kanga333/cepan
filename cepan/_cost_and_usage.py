from typing import Any, Dict, List, Optional, Union

import boto3
import pandas as pd

from cepan import _utils, exceptions
from cepan._filter import Filter, _build_filter
from cepan._group_by import GroupBy, _build_group_by
from cepan._time_period import TimePeriod, _build_time_period


def get_cost_and_usage(
    time_period: Union[TimePeriod, Dict[str, str]],
    granularity: str,
    filter: Union[Filter, Dict[str, Any], None] = None,
    metrics: List[str] = ["UnblendedCost"],
    group_by: Union[GroupBy, List[Dict[str, str]], None] = None,
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    client: boto3.client = _utils.client("ce", session)
    if granularity == "HOURLY":
        raise exceptions.UnsupportedGranularity(
            "Hourly granularity is not yet supported"
        )
    args: Dict[str, Any] = {
        "TimePeriod": _build_time_period(time_period),
        "Granularity": granularity,
        "Metrics": metrics,
    }
    if filter:
        args["Filter"] = _build_filter(filter)
    if group_by:
        args["GroupBy"] = _build_group_by(group_by)
    response_iterator = _utils.call_with_pagination(
        client,
        "get_cost_and_usage",
        args,
    )

    pre_df: List[Dict[str, str]] = []
    for response in response_iterator:
        group_definitions: List[str] = []
        for definition in response.get("GroupDefinitions", []):
            group_definitions.append(definition["Key"])
        for row in response["ResultsByTime"]:
            time: str = row["TimePeriod"]["Start"]
            if row["Total"]:
                processed = _process_total_row(time, row["Total"])
                pre_df.append(processed)
            for group in row["Groups"]:
                processed = _process_group_row(time, group, group_definitions)
                pre_df.append(processed)
    return pd.DataFrame(pre_df, dtype="string")


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
