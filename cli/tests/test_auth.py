import os
import tempfile
from uuid import uuid4

import google
import pytest

from cli.auth.google import get_anon_cred, read_creds, save_creds, get_cred
from cli.config import Config


class Creds:
    def __init__(self, expired=True):
        self.expired = expired
        self.uuid = uuid4()


@pytest.fixture
def valid_cred():
    return Creds(expired=False)


@pytest.fixture
def invalid_cred():
    return Creds()


def test_read_and_save_creds(valid_cred):
    save_creds(valid_cred)
    r_creds = read_creds()
    assert valid_cred.uuid == r_creds.uuid


def test_get_saved_creds(valid_cred):
    save_creds(valid_cred)
    with get_cred(Config.credentials_file) as cred:
        assert not cred.expired


def test_get_anon_creds():
    with get_anon_cred() as cred:
        assert type(cred) == google.auth.credentials.AnonymousCredentials
