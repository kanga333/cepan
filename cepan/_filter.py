from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Union


class Filter(Protocol):
    def build_expression(self) -> Dict[str, Any]:
        ...


@dataclass
class _BaseFilter:
    key: str
    values: List[str]
    match_options: Optional[List[str]] = None

    def _build_base_expression(self) -> Dict[str, Any]:
        filter: Dict[str, Any] = {"Key": self.key, "Values": self.values}
        if self.match_options:
            filter["MatchOptions"] = self.match_options
        return filter


class Dimensions(_BaseFilter):
    """The dimension values used for filtering the costs.
    You can use get_dimension_values to find specific values.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_DimensionValues.html
    """

    def build_expression(self) -> Dict[str, Any]:
        return {"Dimensions": self._build_base_expression()}


class Tags(_BaseFilter):
    """The Tag values used for filtering the costs.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_TagValues.html
    """

    def build_expression(self) -> Dict[str, Any]:
        return {"Tags": self._build_base_expression()}


class CostCategories(_BaseFilter):
    """The Cost Categories values used for filtering the costs.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_CostCategoryValues.html
    """

    def build_expression(self) -> Dict[str, Any]:
        return {"CostCategories": self._build_base_expression()}


@dataclass
class _CompositeFilter:
    filters: List[Filter]

    def _build_composite_expression(self) -> List[Dict[str, Any]]:
        return [f.build_expression() for f in self.filters]


class And(_CompositeFilter):
    """"Return results that match both Filter objects."""

    def build_expression(self) -> Dict[str, Any]:
        return {"And": self._build_composite_expression()}


class Or(_CompositeFilter):
    """Return results that match either Filter object."""

    def build_expression(self) -> Dict[str, Any]:
        return {"Or": self._build_composite_expression()}


@dataclass
class Not:
    """Return results that don't match a Filter object."""

    filter: Filter

    def build_expression(self) -> Dict[str, Any]:
        return {"Not": self.filter.build_expression()}


def _build_filter(filter: Union[Filter, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(filter, Dict):
        return filter
    return filter.build_expression()
