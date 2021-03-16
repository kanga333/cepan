import pytest

from cepan._group_by import GroupBy


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            {
                "dimensions": ["val1", "val2"],
                "tags": [],
                "cost_categories": [],
            },
            [
                {"Type": "DIMENSION", "Key": "val1"},
                {"Type": "DIMENSION", "Key": "val2"},
            ],
        ),
        (
            {
                "dimensions": ["val1"],
                "tags": ["val2"],
                "cost_categories": [],
            },
            [
                {"Type": "DIMENSION", "Key": "val1"},
                {"Type": "TAG", "Key": "val2"},
            ],
        ),
        (
            {
                "dimensions": [],
                "tags": ["val1", "val2"],
                "cost_categories": [],
            },
            [
                {"Type": "TAG", "Key": "val1"},
                {"Type": "TAG", "Key": "val2"},
            ],
        ),
        (
            {
                "dimensions": [],
                "tags": ["val1"],
                "cost_categories": ["val2"],
            },
            [
                {"Type": "TAG", "Key": "val1"},
                {"Type": "COST_CATEGORY", "Key": "val2"},
            ],
        ),
        (
            {
                "dimensions": [],
                "tags": [],
                "cost_categories": ["val1", "val2"],
            },
            [
                {"Type": "COST_CATEGORY", "Key": "val1"},
                {"Type": "COST_CATEGORY", "Key": "val2"},
            ],
        ),
        (
            {
                "dimensions": ["val2"],
                "tags": [],
                "cost_categories": ["val1"],
            },
            [
                {"Type": "DIMENSION", "Key": "val2"},
                {"Type": "COST_CATEGORY", "Key": "val1"},
            ],
        ),
    ],
)
def test_group_by(args, expected):
    f = GroupBy(**args)
    assert f.build() == expected
