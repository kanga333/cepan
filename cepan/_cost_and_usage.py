from typing import Any, Dict, List, Optional, Set, Union

import boto3
import pandas as pd

from cepan import _utils
from cepan._filter import Filter, _build_filter
from cepan._group_by import GroupBy, _build_group_by
from cepan._time_period import TimePeriod, _build_time_period


def get_cost_and_usage(
    time_period: Union[TimePeriod, Dict[str, str]],
    granularity: str,
    filter: Union[Filter, Dict[str, Any], None] = None,
    metrics: List[str] = ["UnblendedCost"],
    group_by: Union[GroupBy, List[Dict[str, str]], None] = None,
    metrics_dtype: str = "float64",
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    """Get cost and usage report.

    See also:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_cost_and_usage

    Parameters
    ----------
    time_period : Union[TimePeriod, Dict[str, str]]
        Sets the start and end dates for retrieving AWS costs.
        In addition to the TimePeriod type,
        you can directly use variables of dictionary types that boto3 can use.
    granularity : str
        Sets the AWS cost granularity to MONTHLY or DAILY , or HOURLY.
    filter : Union[Filter, Dict[str, Any]], optional
        Filters AWS costs by different dimensions.
        In addition to the Filter type,
        you can directly use variables of dictionary types that boto3 can use.
    metrics : List[str], optional
        Which metrics are returned in the query.
    group_by : Union[GroupBy, List[Dict[str, str]]], optional
        You can group AWS costs using up to two different groups.
        In addition to the Filter type,
        you can directly use variables of dictionary types that boto3 can use.
    metrics_dtype: str, optional
        The dtype of metrics. The default is float64.
        If you want to keep the number of significant digits, specify the string type.
    boto3_session : boto3.Session(), optional
        Boto3 Session. The default boto3 session will be used if session receive None.

    Returns
    -------
    pandas.DataFrame
        Result as a Pandas DataFrame.

    Examples
    --------
    >>> import cepan as ce
    >>> from datetime import datetime, timedelta
    >>> today = datetime.now()
    >>> yesterdat = today - timedelta(days=1)
    >>> df = ce.get_cost_and_usage(
    ...     time_period=ce.TimePeriod(
    ...         start=datetime(2020, 1, 1),
    ...         end=datetime(2020, 1, 2),
    ...     ),
    ...     granularity="DAILY",
    ...     filter=ce.Not(ce.Dimensions("SERVICE", ["Amazon Athena"])),
    ...     metrics=["BLENDED_COST", "USAGE_QUANTITY"],
    ...     group_by=ce.GroupBy(["SERVICE", "AZ"]),
    ... )
    """
    client: boto3.client = _utils.client("ce", session)
    args: Dict[str, Any] = {
        "TimePeriod": _build_time_period(time_period, granularity == "HOURLY"),
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
        metrics_columns: Set[str] = set()
        for definition in response.get("GroupDefinitions", []):
            group_definitions.append(definition["Key"])
        for row in response["ResultsByTime"]:
            time: str = row["TimePeriod"]["Start"]
            if row["Total"]:
                processed = _process_total_row(time, row["Total"])
                pre_df.append(processed)
                metrics_columns |= row["Total"].keys()
            for group in row["Groups"]:
                processed = _process_group_row(time, group, group_definitions)
                pre_df.append(processed)
                metrics_columns |= group["Metrics"].keys()
    df = pd.DataFrame(pre_df, dtype="string")
    if metrics_dtype == "string":
        return df
    type_map = {metrics_column: metrics_dtype for metrics_column in metrics_columns}
    return df.astype(type_map)


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
