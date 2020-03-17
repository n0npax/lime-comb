import abc

from lime_comb.api import get_gpgs
from lime_comb.gpg import import_gpg_key


class Command(metaclass=abc.ABCMeta):
    pass


def import_keys(email, cred, *, key_type="pub"):
    for key in get_gpgs(cred, email, key_type=key_type):
        yield from import_gpg_key(key["data"])
