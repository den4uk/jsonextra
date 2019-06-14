import pytest
import io
import uuid
import datetime
# import tempfile
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


def test_dumps():
    assert jsonextra.dumps(dict_example) == json_example


def test_loads():
    assert jsonextra.loads(json_example) == dict_example


def test_load():
    i = io.StringIO(json_example)
    assert jsonextra.load(i) == dict_example


def test_dump():
    i = io.StringIO()
    jsonextra.dump(dict_example, i)
    assert i.getvalue() == json_example


many_list = [
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
