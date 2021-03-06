import pytest

from cepan._utils import call_with_pagination


@pytest.mark.parametrize(
    "pagenation_token",
    ["NextToken", "NextPageToken"],
)
def test_call_with_pagination(mocker, pagenation_token):
    responses = [
        {"Result": "First", pagenation_token: "Second"},
        {"Result": "Second", pagenation_token: "Third"},
        {"Result": "Third"},
    ]
    client_mock = mocker.Mock()
    client_mock.pagenation_method.side_effect = responses
    iterator = call_with_pagination(
        client_mock, "pagenation_method", {"arg1": "foo", "arg2": "bar"}
    )
    assert list(iterator) == responses
    call_list = client_mock.pagenation_method.call_args_list
    keywords_list = [keywords for _, keywords in call_list]
    assert keywords_list == [
        {"arg1": "foo", "arg2": "bar"},
        {"arg1": "foo", "arg2": "bar", pagenation_token: "Second"},
        {"arg1": "foo", "arg2": "bar", pagenation_token: "Third"},
    ]
