jsonextra
=====
[![Build Status](https://travis-ci.org/den4uk/jsonextra.svg?branch=master)](https://travis-ci.org/den4uk/jsonextra)
[![Codecov](https://codecov.io/gh/den4uk/jsonextra/branch/master/graph/badge.svg)](https://codecov.io/gh/den4uk/jsonextra)
[![PyPI Version](http://img.shields.io/pypi/v/jsonextra.svg)](https://pypi.python.org/pypi/jsonextra)
[![License](https://img.shields.io/github/license/den4uk/jsonextra.svg)](https://pypi.python.org/pypi/jsonextra)

_same as `json` library, but with extra support for `bytes`, `uuid` and `datetime` data classes_

## Installation

```
$ pip install jsonextra
```


## Usage

Use just like `json` as normal once imported, but with addition of extra data classes.

```python
import uuid, datetime  # for creation of `my_data` object
import jsonextra

my_data = {'id': uuid.uuid4(), 'created': datetime.date.today()}
# my_data --> {'id': uuid.UUID('5f7660c5-88ea-46b6-93e2-860d5b7a0271'), 'created': datetime.date(2019, 6, 16)}

# Serializes the key values to stringified versions
my_json = jsonextra.dumps(my_data)
# my_json --> '{"id": "5f7660c5-88ea-46b6-93e2-860d5b7a0271", "created": "2019-06-16"}'

# Deserializes the object and confirms the output matches `my_data`
assert jsonextra.loads(my_json) == my_data  # True
```


##### `.dump(obj, fp, **kwargs)` & `.dumps(obj, **kwargs)`
Will serialize extra data classes into their string (`__str__`) or special representations (_eg: `.isoformat`, etc._).


##### `.load(fp, **kwargs)` & `.loads(s, **kwargs)`
Will deserialize any stings, which match patterns of extra supported data classes.
For example, if something looks like a _uuid_ - it will be converted to `uuid.UUID`.
If this behaviour is undesired, please use the built-in `json.loads` method instead of `jsonextra.loads`.


## Supported extra data classes

| Python Data Class | Python Object (deserialized) | JSON Object (serialized) |
|-------------------|------------------------------|--------------------------|
| `datetime.date` | `datetime.date(2019, 1, 1)` | `"2019-01-01"` |
| `datetime.time` | `datetime.time(23, 59, 11)` | `"23:59:11"`  |
| `datetime.datetime` | `datetime.datetime(2019, 1, 1, 23, 59, 11)` | `"2019-01-01T23:59:11"` |
| `uuid.UUID` | `uuid.UUID('5f7660c5-88ea-46b6-93e2-860d5b7a0271')` | `"5f7660c5-88ea-46b6-93e2-860d5b7a0271"` |
| `bytes` | `b'\xd6aO\x1d\xd71Y\x05'` | `"base64:1mFPHdcxWQU="` |

More examples of serialized/deserialized values can be found in tests ;p


## Why?

_Why would you want to use this library?_

- If you work with a model-less data structures, and its data types expend beyond the JSON standard supports.
- If your model schemas are too dynamic to be able to use model-based serializers, and requires to store more data types.
- If your data structure does not fit with the JSON standard, and it needs expanding to support one or more data types.


## How it works

An extra supported python object is dumped to a _string_ value.
When loading a serialized json object, any values matching the string supported data class, will be converted to their expected data class instances.
> _If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck_.


## Contributions

Contibutions are welcome, please submit your pull requests into `dev` branch for a review.
