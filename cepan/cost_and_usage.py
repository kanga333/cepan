from typing import Any, Dict, List, Optional

import boto3
import pandas as pd

from cepan import _utils, exceptions, filter, group_by, time_period


def get_cost_and_usage(
    granularity: str,
    metrics: List[str],
    time_period: time_period.TimePeriod,
    filter: filter.Filter = None,
    group_by: Optional[group_by.GroupBy] = None,
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    client: boto3.client = _utils.client("ce", session)
    if granularity == "HOURLY":
        raise exceptions.UnsupportedGranularity(
            "Hourly granularity is not yet supported"
        )
    args: Dict[str, Any] = {
        "TimePeriod": time_period.build(),
        "Granularity": granularity,
        "Metrics": metrics,
    }
    if filter:
        args["Filter"] = filter.build_expression()
    if group_by:
        args["GroupBy"] = group_by.build()
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
