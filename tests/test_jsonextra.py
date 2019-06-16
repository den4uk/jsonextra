import pytest
import io
import uuid
import datetime
import jsonextra


dict_example = {
    'id': uuid.UUID('d05c6319-0944-4dd6-819f-3a2dc6f7a3c2'),
    'town': 'Hill Valley',
    'episode': 2,
    'date': datetime.date(2015, 10, 21),
    'time': datetime.datetime(2019, 6, 14, 20, 43, 53, 207572),
    'anone': None,
    'watch_again': True,
}

json_example = '{"id": "d05c6319-0944-4dd6-819f-3a2dc6f7a3c2", "town": "Hill Valley", "episode": 2, "date": "2015-10-21", "time": "2019-06-14 20:43:53.207572", "anone": null, "watch_again": true}'


dict_nested = {
    'events': {
        'admin': uuid.UUID('c05c6319-0944-4dd6-819f-3a2dc6f7a3c2'),
        'dates': [datetime.date(2016, 11, 22), datetime.date(2017, 12, 23)],
        'uids': {
            'other': [uuid.UUID('b05c6319-0944-4dd6-819f-3a2dc6f7a3c2'), uuid.UUID('a05c6319-0944-4dd6-819f-3a2dc6f7a3c2')],
            'more': [
                {
                    'a': datetime.date(2018, 1, 24)
                },
                {
                    'b': datetime.date(2019, 2, 25)
                }
            ]
        }
    }
}

json_nested = '{"events": {"admin": "c05c6319-0944-4dd6-819f-3a2dc6f7a3c2", "dates": ["2016-11-22", "2017-12-23"], "uids": {"other": ["b05c6319-0944-4dd6-819f-3a2dc6f7a3c2", "a05c6319-0944-4dd6-819f-3a2dc6f7a3c2"], "more": [{"a": "2018-01-24"}, {"b": "2019-02-25"}]}}}'


def test_load():
    i = io.StringIO(json_example)
    assert jsonextra.load(i) == dict_example


def test_dump():
    i = io.StringIO()
    jsonextra.dump(dict_example, i)
    assert i.getvalue() == json_example


many_list = [
    (dict_example, json_example),
    (dict_nested, json_nested),
    ({'x': 'foo'}, '{"x": "foo"}'),
    ({'x': 2}, '{"x": 2}'),
    ({'x': True}, '{"x": true}'),
    ({'x': None}, '{"x": null}'),
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98f395f2-6ecb-46d8-98e4-926b8dfdd070"}'),
    ({'x': datetime.date(1991, 2, 16)}, '{"x": "1991-02-16"}'),
    ({'x': datetime.datetime(2001, 12, 1, 14, 58, 17)}, '{"x": "2001-12-01 14:58:17"}'),
    ({'x': datetime.datetime(2001, 12, 1, 14, 58, 17, 123456)}, '{"x": "2001-12-01 14:58:17.123456"}'),
]


@pytest.mark.parametrize('py_obj, json_obj', many_list)
def test_dumps_many(py_obj, json_obj):
    assert jsonextra.dumps(py_obj) == json_obj


@pytest.mark.parametrize('py_obj, json_obj', many_list)
def test_loads_many(py_obj, json_obj):
    assert jsonextra.loads(json_obj) == py_obj


odd_cases = [
    ({'x': datetime.datetime(2019, 6, 16, 13, 31, 37)}, '{"x": "2019-06-16T13:31:37"}'),  # Uses ISO8601 as input
    ({'x': datetime.datetime(2019, 6, 16, 13, 31, 37, 6399)}, '{"x": "2019-06-16T13:31:37.006399"}'),  # Uses ISO8601 as input
    ({'x': '2020-12-32'}, '{"x": "2020-12-32"}'),  # Incorrect date
    ({'x': '2019-13-01 25:64:02'}, '{"x": "2019-13-01 25:64:02"}'),  # Incorrect date/time
    ({'x': '00000000-0000-0000-0000-000000000000'}, '{"x": "00000000-0000-0000-0000-000000000000"}'),  # Not correctly structured guid
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F2-6ECB-46D8-98E4-926B8DFDD070"}'),  # Uppercase
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98f395f26ecb46d898e4926b8dfdd070"}'),  # No dashes, but is valid
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F26ECB46D898E4926B8DFDD070"}'),  # As above, uppercase
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F26ecb46d898e4926b8DFDD070"}'),  # As above, mixed case
]


@pytest.mark.parametrize('py_obj, json_obj', odd_cases)
def test_loads_odd_cases(py_obj, json_obj):
    assert jsonextra.loads(json_obj) == py_obj
