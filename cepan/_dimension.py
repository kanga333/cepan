from typing import Any, Dict, List, Optional, Union

import boto3
import pandas as pd

from cepan import _utils, exceptions
from cepan._filter import Filter, _build_filter
from cepan._time_period import TimePeriod, _build_time_period

_COST_AND_USAGE_DIMENSIONS = [
    "AZ",
    "DATABASE_ENGINE",
    "INSTANCE_TYPE",
    "LEGAL_ENTITY_NAME",
    "LINKED_ACCOUNT",
    "OPERATING_SYSTEM",
    "OPERATION",
    "PLATFORM",
    "PURCHASE_TYPE",
    "SERVICE",
    "USAGE_TYPE",
    "USAGE_TYPE_GROUP",
    "REGION",
    "RECORD_TYPE",
    "RESOURCE_ID",
]

_RESERVATIONS_DIMENSIONS = [
    "AZ",
    "CACHE_ENGINE",
    "DEPLOYMENT_OPTION",
    "INSTANCE_TYPE",
    "LINKED_ACCOUNT",
    "PLATFORM",
    "REGION",
    "SCOPE",
    "TAG",
    "TENANCY",
]

_SAVINGS_PLANS_DIMENSIONS = [
    "SAVINGS_PLANS_TYPE",
    "PAYMENT_OPTION",
    "REGION",
    "INSTANCE_TYPE_FAMILY",
    "LINKED_ACCOUNT",
    "SAVINGS_PLAN_ARN",
]


def show_dimensions(context: str = "COST_AND_USAGE") -> List[str]:
    """Show dimension keys.

    Parameters
    ----------
    context : str
        The context for the call to get_dimension_values .
        This can be RESERVATIONS, COST_AND_USAGE or SAVINGS_PLANS.

    Returns
    -------
    List[str]
        Result as a Pandas DataFrame.

    """
    if context == "COST_AND_USAGE":
        return _COST_AND_USAGE_DIMENSIONS
    if context == "RESERVATIONS":
        return _RESERVATIONS_DIMENSIONS
    if context == "SAVINGS_PLANS":
        return _SAVINGS_PLANS_DIMENSIONS
    raise exceptions.InvalidParameter(
        f"{context} is invalid, valid values are COST_AND_USAGE, RESERVATIONS, SAVINGS_PLANS."  # noqa
    )


def get_dimension_values(
    time_period: Union[TimePeriod, Dict[str, str]],
    dimension: str,
    search_string: Optional[str] = None,
    context: Optional[str] = None,
    filter: Union[Filter, Dict[str, Any], None] = None,
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    """Get dimension values.

    See also:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_dimension_values

    Parameters
    ----------
    time_period : Union[TimePeriod, Dict[str, str]]
        Sets the start and end dates for retrieving AWS costs.
        In addition to the TimePeriod type,
        you can directly use variables of dictionary types that boto3 can use.
    dimension : str
        The name of the dimension. Each dimension is available for a different context.
    search_string : str
        The value that you want to search the filter values for.
    context : str
        The context for the call to get_dimension_values.
        This can be RESERVATIONS, COST_AND_USAGE or SAVINGS_PLANS.
    filter : Union[Filter, Dict[str, Any]], optional
        Filters AWS costs by different dimensions.
        In addition to the Filter type,
        you can directly use variables of dictionary types that boto3 can use.
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
    >>> df = ce.get_dimension_values(
    ...     time_period=ce.TimePeriod(
    ...         start=datetime(2020, 1, 1),
    ...         end=datetime(2020, 1, 2),
    ...     ),
    ...     dimension="SERVICE",
    ...     search_string="Amazon",
    ... )
    """
    client: boto3.client = _utils.client("ce", session)
    args: Dict[str, Any] = {
        "TimePeriod": _build_time_period(time_period),
        "Dimension": dimension,
    }
    if search_string:
        args["SearchString"] = search_string
    if context:
        args["Context"] = context
    if filter:
        args["Filter"] = _build_filter(filter)
    response_iterator = _utils.call_with_pagination(
        client,
        "get_dimension_values",
        args,
    )

    pre_df: List[Dict[str, str]] = []
    for response in response_iterator:
        for row in response["DimensionValues"]:
            if not row["Value"]:
                continue
            pre_row: Dict[str, str] = {"dimension": dimension}
            pre_row["value"] = row["Value"]
            pre_df.append(pre_row)
        return pd.DataFrame(pre_df, dtype="string")
