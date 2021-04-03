import pytest

from cepan._filter import (
    And,
    CostCategories,
    Dimensions,
    Not,
    Or,
    Tags,
    _BaseFilter,
    _CompositeFilter,
)


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            {"key": "key", "values": ["value1", "value2"]},
            {"Key": "key", "Values": ["value1", "value2"]},
        ),
        (
            {"key": "key", "values": ["value1"], "match_options": ["EQUALS"]},
            {"Key": "key", "Values": ["value1"], "MatchOptions": ["EQUALS"]},
        ),
    ],
)
def test_basefilter(args, expected):
    f = _BaseFilter(**args)
    assert f._build_base_expression() == expected


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            {"key": "key", "values": ["value1"]},
            {"Dimensions": {"Key": "key", "Values": ["value1"]}},
        ),
        (
            {"key": "SERVICE", "values": ["EC2", "S3"]},
            {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": [
                        "Amazon Elastic Compute Cloud - Compute",
                        "Amazon Simple Storage Service",
                    ],
                }
            },
        ),
    ],
)
def test_dimensions(args, expected):
    f = Dimensions(**args)
    assert f.build_expression() == expected


def test_tags():
    f = Tags("key", ["value1"])
    assert f.build_expression() == {"Tags": {"Key": "key", "Values": ["value1"]}}


def test_costcategories():
    f = CostCategories("key", ["value1"])
    assert f.build_expression() == {
        "CostCategories": {"Key": "key", "Values": ["value1"]}
    }


@pytest.mark.parametrize(
    "filters,expected",
    [
        (
            [
                Dimensions("key1", ["value1"]),
            ],
            [
                {"Dimensions": {"Key": "key1", "Values": ["value1"]}},
            ],
        ),
        (
            [
                Dimensions("key1", ["value1"]),
                Dimensions("key2", ["value2"]),
            ],
            [
                {"Dimensions": {"Key": "key1", "Values": ["value1"]}},
                {"Dimensions": {"Key": "key2", "Values": ["value2"]}},
            ],
        ),
        (
            [
                Dimensions("key1", ["value1"]),
                And(
                    [
                        Dimensions("key2", ["value2"]),
                        Dimensions("key3", ["value3"]),
                    ]
                ),
            ],
            [
                {"Dimensions": {"Key": "key1", "Values": ["value1"]}},
                {
                    "And": [
                        {"Dimensions": {"Key": "key2", "Values": ["value2"]}},
                        {"Dimensions": {"Key": "key3", "Values": ["value3"]}},
                    ]
                },
            ],
        ),
    ],
)
def test_compositefilter(filters, expected):
    f = _CompositeFilter(filters)
    assert f._build_composite_expression() == expected


def test_and():
    f = And([Dimensions("key", ["value"])])
    assert f.build_expression() == {
        "And": [{"Dimensions": {"Key": "key", "Values": ["value"]}}]
    }


def test_or():
    f = Or([Dimensions("key", ["value"])])
    assert f.build_expression() == {
        "Or": [{"Dimensions": {"Key": "key", "Values": ["value"]}}]
    }


def test_not():
    f = Not(Dimensions("key", ["value"]))
    assert f.build_expression() == {
        "Not": {"Dimensions": {"Key": "key", "Values": ["value"]}}
    }
