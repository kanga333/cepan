from typing import Any, Dict, List, Optional, Union

import boto3
import pandas as pd

from cepan import _utils
from cepan._filter import Filter, _build_filter
from cepan._time_period import TimePeriod, _build_time_period


def get_tags(
    time_period: Union[TimePeriod, Dict[str, str]],
    tag_key: str,
    search_string: Optional[str] = None,
    filter: Union[Filter, Dict[str, Any], None] = None,
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    """Get tag values.

    See also:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client.get_dimension_values

    Parameters
    ----------
    time_period : Union[TimePeriod, Dict[str, str]]
        Sets the start and end dates for retrieving AWS costs.
        In addition to the TimePeriod type,
        you can directly use variables of dictionary types that boto3 can use.
    tag_key : str
        The key of the tag that you want to return values for.
    search_string : str
        The value that you want to search the filter values for.
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
    >>> df = ce.get_tags(
    ...     time_period=ce.TimePeriod(
    ...         start=datetime(2020, 1, 1),
    ...         end=datetime(2020, 1, 2),
    ...     ),
    ...     tag_key="Owner",
    ... )
    """
    client: boto3.client = _utils.client("ce", session)
    args: Dict[str, Any] = {
        "TimePeriod": _build_time_period(time_period),
        "TagKey": tag_key,
    }
    if search_string:
        args["SearchString"] = search_string
    if filter:
        args["Filter"] = _build_filter(filter)
    response_iterator = _utils.call_with_pagination(
        client,
        "get_tags",
        args,
    )

    pre_df: List[Dict[str, str]] = []
    for response in response_iterator:
        for row in response["Tags"]:
            if not row:
                continue
            pre_row: Dict[str, str] = {"tag_key": tag_key}
            pre_row["value"] = row
            pre_df.append(pre_row)
        return pd.DataFrame(pre_df, dtype="string")
