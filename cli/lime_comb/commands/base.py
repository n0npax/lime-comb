import abc
import argparse
import os

import email_validator

from lime_comb.firestore.database import get_gpgs
from lime_comb.gpg import import_gpg_key


class Command(metaclass=abc.ABCMeta):
    pass


def import_keys(email, cred, *, key_type="pub"):
    for key_str in get_gpgs(cred, email, key_type=key_type):
        yield from import_gpg_key(key_str)


def validate_filepath(fp):
    if not os.path.isfile(fp):
        raise argparse.ArgumentTypeError(f"have to be file")
    return fp


def validate_email(email):
    email_validator.validate_email(email)
    return email
