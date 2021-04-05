from typing import Dict, List, Optional

import pandas as pd

_SERVICE_ALIAS = {
    "Amazon Athena": [
        "Athena",
    ],
    "Amazon CloudFront": [
        "CloudFront",
    ],
    "Amazon DynamoDB": [
        "DynamoDB",
    ],
    "Amazon EC2 Container Registry (ECR)": [
        "ECR",
        "EC2 Container Registry",
    ],
    "Amazon Elastic Compute Cloud - Compute": [
        "EC2",
        "EC2-Instances",
        "Elastic Compute Cloud - Compute",
    ],
    "Amazon Elastic Container Service": [
        "ECS",
        "Elastic Container Service",
    ],
    "Amazon Elastic File System": [
        "EFS",
        "Elastic File System",
    ],
    "Amazon Elastic Load Balancing": [
        "ELB",
        "EC2-ELB",
        "Elastic Load Balancing",
    ],
    "Amazon Elastic MapReduce": [
        "EMR",
        "Elastic MapReduce",
    ],
    "Amazon ElastiCache": [
        "ElastiCache",
    ],
    "Amazon Elasticsearch Service": [
        "ES",
        "Amazon ES",
        "Elasticsearch Service",
    ],
    "Amazon GuardDuty": [
        "GuardDuty",
    ],
    "Amazon Kinesis": [
        "Kinesis",
    ],
    "Amazon Managed Streaming for Apache Kafka": [
        "MSK",
        "Amazon MSK",
        "Managed Streaming for Apache Kafka",
    ],
    "Amazon Redshift": [
        "Redshift",
    ],
    "Amazon Relational Database Service": [
        "RDS",
        "Relational Database Service",
    ],
    "Amazon Route 53": [
        "Route 53",
    ],
    "Amazon SageMaker": [
        "SageMaker",
    ],
    "Amazon Simple Notification Service": [
        "SNS",
        "Simple Notification Service",
    ],
    "Amazon Simple Queue Service": [
        "SQS",
        "Simple Queue Services",
    ],
    "Amazon Simple Storage Service": [
        "S3",
        "Simple Storage Service",
    ],
    "AmazonCloudWatch": [
        "CloudWatch",
    ],
    "AWS Budgets": [
        "Budgets",
    ],
    "AWS CloudTrail": [
        "CloudTrail",
    ],
    "AWS Config": [
        "Config",
    ],
    "AWS Cost Explorer": [
        "Cost Explorer",
    ],
    "AWS Data Transfer": [
        "Data Transfer",
    ],
    "AWS Elemental MediaStore": [
        "Elemental MediaStore",
    ],
    "AWS Glue": [
        "Glue",
    ],
    "AWS Key Management Service": [
        "KMS",
        "Key Management Service",
    ],
    "AWS Lambda": [
        "Lambda",
    ],
    "AWS Secrets Manager": [
        "Secrets Manager",
    ],
    "AWS Security Hub": [
        "Security Hub",
    ],
    "AWS Service Catalog": [
        "Service Catalog",
    ],
    "AWS Step Functions": [
        "Step Functions",
    ],
    "EC2 - Other": [
        "EC2-Other",
    ],
}

_SERVICE_ALIAS_TABLE: Optional[Dict[str, str]] = None


def show_service_alias() -> pd.DataFrame:
    """Show a list of aliases for aws service names.

    Returns
    -------
    pandas.DataFrame
        DataFrame with the corresponding proper name and alias

    """
    pre_df: List[Dict[str, str]] = []
    for key, aliases in _SERVICE_ALIAS.items():
        pre_row: Dict[str, str] = {"service_name": key, "aliases": ",".join(aliases)}
        pre_df.append(pre_row)
    return pd.DataFrame(pre_df, dtype="string")


def _resolve_service_alias(service_name: str) -> str:
    alias_table = _get_service_alias_table()
    return alias_table.get(service_name, service_name)


def _get_service_alias_table() -> Dict[str, str]:
    global _SERVICE_ALIAS_TABLE
    if _SERVICE_ALIAS_TABLE:
        return _SERVICE_ALIAS_TABLE

    service_alias_table: Dict[str, str] = {}
    for key, aliases in _SERVICE_ALIAS.items():
        for alias in aliases:
            service_alias_table[alias] = key

    _SERVICE_ALIAS_TABLE = service_alias_table
    return _SERVICE_ALIAS_TABLE
