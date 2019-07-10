import pytest
import io
import uuid
import secrets
import datetime
import jsonextra


dict_flat = {
    'id': uuid.UUID('d05c6319-0944-4dd6-819f-3a2dc6f7a3c2'),
    'town': 'Hill Valley',
    'episode': 2,
    'date': datetime.date(2015, 10, 21),
    'datetime': datetime.datetime(2019, 6, 14, 20, 43, 53, 207572),
    'time': datetime.time(12, 34, 56),
    'secret': b'\xd6aO\x1d\xd71Y\x05',
    'anone': None,
    'watch_again': True,
}

json_flat = '''{
  "id": "d05c6319-0944-4dd6-819f-3a2dc6f7a3c2",
  "town": "Hill Valley",
  "episode": 2,
  "date": "2015-10-21",
  "datetime": "2019-06-14T20:43:53.207572",
  "time": "12:34:56",
  "secret": "base64:1mFPHdcxWQU=",
  "anone": null,
  "watch_again": true
}'''


dict_nested = {
    'events': {
        'admin': uuid.UUID('c05c6319-0944-4dd6-819f-3a2dc6f7a3c2'),
        'dates': [
            datetime.date(2016, 11, 22),
            datetime.date(2017, 12, 23)
        ],
        'uids': {
            'other': [
                uuid.UUID('b05c6319-0944-4dd6-819f-3a2dc6f7a3c2'),
                uuid.UUID('a05c6319-0944-4dd6-819f-3a2dc6f7a3c2')
            ],
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


json_nested = '''{
  "events": {
    "admin": "c05c6319-0944-4dd6-819f-3a2dc6f7a3c2",
    "dates": [
      "2016-11-22",
      "2017-12-23"
    ],
    "uids": {
      "other": [
        "b05c6319-0944-4dd6-819f-3a2dc6f7a3c2",
        "a05c6319-0944-4dd6-819f-3a2dc6f7a3c2"
      ],
      "more": [
        {
          "a": "2018-01-24"
        },
        {
          "b": "2019-02-25"
        }
      ]
    }
  }
}'''


@pytest.mark.parametrize('py_obj, json_obj', [
    (dict_flat, json_flat),
    (dict_nested, json_nested),
])
def test_load(py_obj, json_obj):
    i = io.StringIO(json_obj)
    assert jsonextra.load(i) == py_obj


@pytest.mark.parametrize('py_obj, json_obj', [
    (dict_flat, json_flat),
    (dict_nested, json_nested),
])
def test_dump(py_obj, json_obj):
    i = io.StringIO()
    jsonextra.dump(py_obj, i, indent=2)
    assert i.getvalue() == json_obj


many_list = [
    ({'x': 'foo'}, '{"x": "foo"}'),
    ({'x': 2}, '{"x": 2}'),
    ({'x': True}, '{"x": true}'),
    ({'x': None}, '{"x": null}'),
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98f395f2-6ecb-46d8-98e4-926b8dfdd070"}'),
    ({'x': datetime.date(1991, 2, 16)}, '{"x": "1991-02-16"}'),
    ({'x': datetime.datetime(2001, 12, 1, 14, 58, 17)}, '{"x": "2001-12-01T14:58:17"}'),
    ({'x': datetime.datetime(2001, 12, 1, 14, 58, 17, 123456)}, '{"x": "2001-12-01T14:58:17.123456"}'),
    ({'x': datetime.time(9, 12, 4)}, '{"x": "09:12:04"}'),
    ({'x': datetime.time(23, 52, 43)}, '{"x": "23:52:43"}'),
    ({'x': datetime.time(0)}, '{"x": "00:00:00"}'),
    ({'x': datetime.time(0, 1, 0, 1001)}, '{"x": "00:01:00.001001"}'),
    ({'x': b'hello'}, '{"x": "base64:aGVsbG8="}'),
    ({'x': b''}, '{"x": "base64:"}'),
]


@pytest.mark.parametrize('py_obj, json_obj', many_list)
def test_dumps_many(py_obj, json_obj):
    assert jsonextra.dumps(py_obj) == json_obj


@pytest.mark.parametrize('py_obj, json_obj', many_list)
def test_loads_many(py_obj, json_obj):
    assert jsonextra.loads(json_obj) == py_obj


odd_cases = [
    ({'x': datetime.datetime(2019, 6, 16, 13, 31, 37)}, '{"x": "2019-06-16 13:31:37"}'),  # iso8601 without the `T`
    ({'x': datetime.datetime(2019, 6, 16, 13, 31, 37, 6399)}, '{"x": "2019-06-16 13:31:37.006399"}'),  # iso8601 without the `T`
    ({'x': '24:23:22'}, '{"x": "24:23:22"}'),  # Incorrect time
    ({'x': '2020-12-32'}, '{"x": "2020-12-32"}'),  # Incorrect date
    ({'x': '2019-13-01 25:64:02'}, '{"x": "2019-13-01 25:64:02"}'),  # Incorrect date/time
    ({'x': '00000000-0000-0000-0000-000000000000'}, '{"x": "00000000-0000-0000-0000-000000000000"}'),  # Not correctly structured guid
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F2-6ECB-46D8-98E4-926B8DFDD070"}'),  # Uppercase
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98f395f26ecb46d898e4926b8dfdd070"}'),  # No dashes, but is valid
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F26ECB46D898E4926B8DFDD070"}'),  # As above, uppercase
    ({'x': uuid.UUID('98f395f2-6ecb-46d8-98e4-926b8dfdd070')}, '{"x": "98F395F26ecb46d898e4926b8DFDD070"}'),  # As above, mixed case
    ({'x': 'base64:Oly==='}, '{"x": "base64:Oly==="}'),  # invalid base64 string (too much padding)
]


@pytest.mark.parametrize('py_obj, json_obj', odd_cases)
def test_loads_odd_cases(py_obj, json_obj):
    assert jsonextra.loads(json_obj) == py_obj


def test_random_bytes():
    for n in range(128):
        my_obj = {'x': secrets.token_bytes(n)}
        serialized = jsonextra.dumps(my_obj)
        assert jsonextra.loads(serialized) == my_obj
