from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class SortBy:
    """The value by which you want to sort the data.
    See also:
    https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_SortDefinition.html
    """

    key: str
    sort_order: Optional[str] = None

    def build(self) -> Dict[str, str]:
        sort_by: Dict[str, str] = {"Key": self.key}
        if self.sort_order:
            sort_by["SortOrder"] = self.sort_order
        return sort_by


def _build_sort_by(
    sort_by: Union[List[SortBy], List[Dict[str, str]]]
) -> List[Dict[str, str]]:
    builded: List[Dict[str, str]] = []
    for item in sort_by:
        if isinstance(item, Dict):
            builded.append(item)
        else:
            builded.append(item.build())
    return builded
