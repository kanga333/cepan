import datetime
from typing import Any, Dict, List, Optional

import boto3
import pandas as pd

_DIMENSIONS = [
    "AZ",
    "INSTANCE_TYPE",
    "LINKED_ACCOUNT",
    "LINKED_ACCOUNT_NAME",
    "OPERATION",
    "PURCHASE_TYPE",
    "REGION",
    "SERVICE",
    "SERVICE_CODE",
    "USAGE_TYPE",
    "USAGE_TYPE_GROUP",
    "RECORD_TYPE",
    "OPERATING_SYSTEM",
    "TENANCY",
    "SCOPE",
    "PLATFORM",
    "SUBSCRIPTION_ID",
    "LEGAL_ENTITY_NAME",
    "DEPLOYMENT_OPTION",
    "DATABASE_ENGINE",
    "CACHE_ENGINE",
    "INSTANCE_TYPE_FAMILY",
    "BILLING_ENTITY",
    "RESERVATION_ID",
    "RESOURCE_ID",
    "RIGHTSIZING_TYPE",
    "SAVINGS_PLANS_TYPE",
    "SAVINGS_PLAN_ARN",
    "PAYMENT_OPTION",
    "AGREEMENT_END_DATE_TIME_AFTER",
    "AGREEMENT_END_DATE_TIME_BEFORE",
]


def get_dimensions() -> pd.DataFrame:
    return pd.DataFrame(_DIMENSIONS, columns=["dimensions"])


def get_dimension_values(
    dimension: str,
    start: datetime.date,
    end: datetime.date = datetime.date.today(),
    search_string: Optional[str] = None,
) -> pd.DataFrame:
    args: Dict[str, Any] = {
        "TimePeriod": {"Start": start.isoformat(), "End": end.isoformat()},
        "Dimension": dimension,
    }
    client: boto3.client = boto3.client("ce")
    response: Dict[str, Any] = client.get_dimension_values(**args)
    pre_df: List[Dict[str, str]] = []
    for row in response["DimensionValues"]:
        if not row["Value"]:
            continue
        pre_row: Dict[str, str] = {"dimension": dimension}
        pre_row["value"] = row["Value"]
        pre_df.append(pre_row)
    return pd.DataFrame(pre_df, dtype="string")