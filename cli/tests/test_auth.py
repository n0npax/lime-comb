import os
import tempfile

import google
import pytest

from cli.auth.google import get_anon_cred, read_creds, save_creds
from cli.config import Config


def test_read_and_save_creds():
    creds = {"mocked": "credentials"}
    save_creds(creds)
    r_creds = read_creds()
    assert creds == r_creds


def test_get_anon_creds():
    with get_anon_cred() as cred:
        assert type(cred) == google.auth.credentials.AnonymousCredentials
