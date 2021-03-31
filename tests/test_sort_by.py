import pytest

from cepan._sort_by import SortBy


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            {"key": "BlendedCost"},
            {"Key": "BlendedCost"},
        ),
        (
            {
                "key": "UnblendedCost",
                "sort_order": "ASCENDING",
            },
            {"Key": "UnblendedCost", "SortOrder": "ASCENDING"},
        ),
    ],
)
def test_sort_by(args, expected):
    t = SortBy(**args)
    assert t.build() == expected
