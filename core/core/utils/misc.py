from django.conf import settings
from django.db import transaction
import yaml


def yaml_coerce(value):
    # Convert value to proper python
    if isinstance(value, str):
        # Yaml.load returns a Python object
        # Convert string dict to python dict
        # Useful because sometime we need to stringify this way like in docker file
        return yaml.load('dummy: ' + value, Loader=yaml.SafeLoader)['dummy']

    return value


def hex_to_bytes(hex_string: str) -> bytes:
    return bytes.fromhex(hex_string)


def bytes_to_hex(bytes_: bytes) -> str:
    return bytes(bytes_).hex()


def apply_on_commit(callable_):
    if settings.USE_ON_COMMIT_HOOK:
        transaction.on_commit(callable_)
    else:
        callable_()
