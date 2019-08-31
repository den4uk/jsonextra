import re
import json
import uuid
import base64
import datetime
import contextlib
import dateutil.parser

uuid_rex = re.compile(r'^[0-9a-f]{8}\-?[0-9a-f]{4}\-?4[0-9a-f]{3}\-?[89ab][0-9a-f]{3}\-?[0-9a-f]{12}$', re.I)
datetime_rex = re.compile(r'^\d{4}\-[01]\d\-[0-3]\d[\sT][0-2]\d\:[0-5]\d\:[0-5]\d')
date_rex = re.compile(r'^\d{4}\-[01]\d\-[0-3]\d$')
time_rex = re.compile(r'^[0-2]\d\:[0-5]\d:[0-5]\d\.?\d{,6}?$')
BYTES_PREFIX = 'base64:'
bytes_rex = re.compile(BYTES_PREFIX + r'([\w\d\+/]*?\={,2}?)$', re.DOTALL)

_all_rex = ['uuid_rex', 'datetime_rex', 'date_rex', 'time_rex', 'bytes_rex']


def disable_rex(rex):
    """Disables a regulax expresseion for matching"""
    assert rex in _all_rex, f'Cannot disable rex which is not allowed! Available: {_all_rex}'
    globals()[rex] = None


class ExtraEncoder(json.JSONEncoder):

    @staticmethod
    def bytes_to_b64(data: bytes) -> str:
        return base64.b64encode(data).decode()

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if isinstance(obj, bytes):
                return (BYTES_PREFIX + self.bytes_to_b64(obj))
            elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
                return obj.isoformat()
            return str(obj)


class ExtraDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)

    @staticmethod
    def _apply_extras(value: str):
        with contextlib.suppress(ValueError):
            if uuid_rex and uuid_rex.match(value):
                return uuid.UUID(value)
            elif date_rex and date_rex.match(value):
                return dateutil.parser.parse(value).date()
            elif datetime_rex and datetime_rex.match(value):
                return dateutil.parser.parse(value)
            elif time_rex and time_rex.match(value):
                return dateutil.parser.parse(value).time()
            elif bytes_rex:
                try_bytes = bytes_rex.match(value)
                if try_bytes:
                    return base64.b64decode(try_bytes.groups()[0])
        return value

    def object_hook(self, obj):
        for key, value in obj.items():
            if isinstance(value, str):
                obj[key] = self._apply_extras(value)
            elif isinstance(value, (list, tuple)):
                for n, v in enumerate(value):
                    if isinstance(v, str):
                        obj[key][n] = self._apply_extras(v)
        return obj


def dumps(*args, **kwargs):
    kwargs['cls'] = kwargs.pop('cls', ExtraEncoder)
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs['cls'] = kwargs.pop('cls', ExtraEncoder)
    return json.dump(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs['cls'] = kwargs.pop('cls', ExtraDecoder)
    return json.loads(*args, **kwargs)


def load(*args, **kwargs):
    kwargs['cls'] = kwargs.pop('cls', ExtraDecoder)
    return json.load(*args, **kwargs)
