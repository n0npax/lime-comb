import os
import tempfile
from uuid import uuid4

import google
import pytest

from cli.auth.google import get_anon_cred, read_creds, save_creds
from cli.config import Config


class Creds:
    def __init__(self):
        self.expired = True
        self.uuid = uuid4()


def test_read_and_save_creds():
    creds = Creds()
    save_creds(creds)
    r_creds = read_creds()
    assert creds.uuid == r_creds.uuid


def test_get_anon_creds():
    with get_anon_cred() as cred:
        assert type(cred) == google.auth.credentials.AnonymousCredentials
