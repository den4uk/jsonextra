import re
import json
import uuid
import base64
import datetime
import contextlib
import dateutil.parser
from typing import Union


class _RegexManager:
    BYTES_PREFIX = 'base64:'
    REGEX = {
        'uuid_rex': re.compile(r'^[0-9a-f]{8}\-?[0-9a-f]{4}\-?4[0-9a-f]{3}\-?[89ab][0-9a-f]{3}\-?[0-9a-f]{12}$', re.I),
        'datetime_rex': re.compile(r'^\d{4}\-[01]\d\-[0-3]\d[\sT][0-2]\d\:[0-5]\d\:[0-5]\d'),
        'date_rex': re.compile(r'^\d{4}\-[01]\d\-[0-3]\d$'),
        'time_rex': re.compile(r'^[0-2]\d\:[0-5]\d:[0-5]\d\.?\d{,6}?$'),
        'bytes_rex': re.compile(BYTES_PREFIX + r'([\w\d\+/]*?\={,2}?)$', re.DOTALL),
    }
    registry = {k: True for k in REGEX.keys()}

    @classmethod
    def is_match(cls, rex_name: str, value: object, return_value: bool = False) -> bool:
        rex = cls.REGEX.get(rex_name)
        if rex and cls.registry[rex_name] and rex.match(value):
            return True
        return False

    @classmethod
    def get_match(cls, rex_name: str, value: object) -> Union[re.Match, None]:
        rex = cls.REGEX.get(rex_name)
        if rex and cls.registry[rex_name]:
            return rex.match(value)

    @classmethod
    def toggle_rex(cls, rex_name: str, value: bool) -> None:
        assert rex_name in cls.registry, f'Unknown regex name supplied. Available: {[*cls.registry]}'
        cls.registry[rex_name] = value

    @classmethod
    def disable_rex(cls, rex_name: str) -> None:
        cls.toggle_rex(rex_name, False)

    @classmethod
    def enable_rex(cls, rex_name: str) -> None:
        cls.toggle_rex(rex_name, True)


def disable_rex(rex):
    """Disables a regulax expresseion for matching"""
    _RegexManager.disable_rex(rex)


def enable_rex(rex):
    """Enables a regulax expresseion for matching"""
    _RegexManager.enable_rex(rex)


class ExtraEncoder(json.JSONEncoder):

    @staticmethod
    def bytes_to_b64(data: bytes) -> str:
        return base64.b64encode(data).decode()

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            if isinstance(obj, bytes):
                return (_RegexManager.BYTES_PREFIX + self.bytes_to_b64(obj))
            elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
                return obj.isoformat()
            return str(obj)


class ExtraDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)

    @staticmethod
    def _apply_extras(value: str):
        with contextlib.suppress(ValueError):
            if _RegexManager.is_match('uuid_rex', value):
                return uuid.UUID(value)
            elif _RegexManager.is_match('date_rex', value):
                return dateutil.parser.parse(value).date()
            elif _RegexManager.is_match('datetime_rex', value):
                return dateutil.parser.parse(value)
            elif _RegexManager.is_match('time_rex', value):
                return dateutil.parser.parse(value).time()
            elif _RegexManager.registry['bytes_rex']:
                bytes_match = _RegexManager.get_match('bytes_rex', value)
                if bytes_match:
                    return base64.b64decode(bytes_match.groups()[0])
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
