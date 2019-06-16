JSON Extra
=====
[![Build Status](https://travis-ci.org/den4uk/jsonextra.svg?branch=master)](https://travis-ci.org/den4uk/jsonextra)
[![Coverage Status](https://coveralls.io/repos/github/den4uk/jsonextra/badge.svg?branch=master)](https://coveralls.io/github/den4uk/jsonextra?branch=master)
[![PyPI version](https://badge.fury.io/py/jsonextra.svg)](https://badge.fury.io/py/jsonextra)

## Installation

```
$ pip install jsonextra
```


## Usage

Use just like `json` as normal once imported

```python
import uuid, datetime  # for creation of `my_data` object
import jsonextra as json

my_data = {'id': uuid.uuid4(), 'created': datetime.date.today()}
# my_data --> {'id': uuid.UUID('5f7660c5-88ea-46b6-93e2-860d5b7a0271'), 'created': datetime.date(2019, 6, 16)}

# Serializes the key values to stringified versions
my_json = json.dumps(my_data)
# my_json --> '{"id": "5f7660c5-88ea-46b6-93e2-860d5b7a0271", "created": "2019-06-16"}'

# Deserializes the object and confirms the output matches `my_data`
assert json.loads(my_json) == my_data  # True
```


## Extra supported data types

- datetime.date
- datetime.datetime
- uuid.UUID
