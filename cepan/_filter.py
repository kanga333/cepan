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
    def build_expression(self) -> Dict[str, Any]:
        return {"Dimensions": self._build_base_expression()}


class Tags(_BaseFilter):
    def build_expression(self) -> Dict[str, Any]:
        return {"Tags": self._build_base_expression()}


class CostCategories(_BaseFilter):
    def build_expression(self) -> Dict[str, Any]:
        return {"CostCategories": self._build_base_expression()}


@dataclass
class _CompositeFilter:
    filters: List[Filter]

    def _build_composite_expression(self) -> List[Dict[str, Any]]:
        return [f.build_expression() for f in self.filters]


class And(_CompositeFilter):
    def build_expression(self) -> Dict[str, Any]:
        return {"And": self._build_composite_expression()}


class Or(_CompositeFilter):
    def build_expression(self) -> Dict[str, Any]:
        return {"Or": self._build_composite_expression()}


@dataclass
class Not:
    filter: Filter

    def build_expression(self) -> Dict[str, Any]:
        return {"Not": self.filter.build_expression()}


def _build_filter(filter: Union[Filter, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(filter, Dict):
        return filter
    return filter.build_expression()
