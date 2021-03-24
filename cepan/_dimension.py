from typing import Any, Dict, List, Optional

import boto3
import pandas as pd

from cepan import _time_period, _utils, exceptions

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
    dimension: str,
    time_period: _time_period.TimePeriod,
    search_string: Optional[str] = None,
    session: Optional[boto3.Session] = None,
) -> pd.DataFrame:
    client: boto3.client = _utils.client("ce", session)
    args: Dict[str, Any] = {
        "TimePeriod": time_period.build(),
        "Dimension": dimension,
    }
    response: Dict[str, Any] = client.get_dimension_values(**args)
    pre_df: List[Dict[str, str]] = []
    for row in response["DimensionValues"]:
        if not row["Value"]:
            continue
        pre_row: Dict[str, str] = {"dimension": dimension}
        pre_row["value"] = row["Value"]
        pre_df.append(pre_row)
    return pd.DataFrame(pre_df, dtype="string")
