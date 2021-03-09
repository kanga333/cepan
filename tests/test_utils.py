import datetime

from cepan._utils import build_date_period, call_with_pagination


def test_build_date_period():
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 1, 2)
    assert build_date_period(start, end) == {
        "Start": "2020-01-01",
        "End": "2020-01-02",
    }


def test_call_with_pagination(mocker):
    responses = [
        {"Result": "First", "NextToken": "Second"},
        {"Result": "Second", "NextToken": "Third"},
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
        {"arg1": "foo", "arg2": "bar", "NextToken": "Second"},
        {"arg1": "foo", "arg2": "bar", "NextToken": "Third"},
    ]
