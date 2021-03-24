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
