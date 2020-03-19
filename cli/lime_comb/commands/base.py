import abc

import lime_comb.api as api
import lime_comb.gpg as gpg


class Command(metaclass=abc.ABCMeta):
    pass


def import_keys(email, cred, *, key_type="pub"):
    for key in api.get_gpgs(cred, email, key_type=key_type):
        yield from gpg.import_gpg_key(key["data"])
