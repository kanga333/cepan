from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class GroupBy:
    """Represents a group when you specify a group by criteria or
    in the response to a query with a specific grouping.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GroupDefinition.html
    """

    dimensions: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    cost_categories: Optional[List[str]] = None

    def build(self) -> List[Dict[str, str]]:
        group_by: List[Dict[str, str]] = []
        if self.dimensions:
            for dimension in self.dimensions:
                group_by.append({"Type": "DIMENSION", "Key": dimension})
        if self.tags:
            for tag in self.tags:
                group_by.append({"Type": "TAG", "Key": tag})
        if self.cost_categories:
            for cost_category in self.cost_categories:
                group_by.append({"Type": "COST_CATEGORY", "Key": cost_category})
        return group_by


def _build_group_by(
    _group_by: Union[GroupBy, List[Dict[str, str]]]
) -> List[Dict[str, str]]:
    if isinstance(_group_by, List):
        return _group_by
    return _group_by.build()
