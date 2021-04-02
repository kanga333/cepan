import cepan as ce
from cepan._alias import _resolve_service_alias


def test_show_service_alias(mocker):
    df = ce.show_service_alias()
    assert len(df.columns) == 2


def test_resolve_service_alias(mocker):
    expected = "Amazon Elastic Compute Cloud - Compute"
    for key in [
        "EC2",
        "EC2-Instances",
        "Elastic Compute Cloud - Compute",
        "Amazon Elastic Compute Cloud - Compute",
    ]:
        name = _resolve_service_alias(key)
        assert name == expected
