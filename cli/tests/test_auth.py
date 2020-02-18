import os
import tempfile

import pytest

from cli.config import Config
from cli.auth.google import read_creds, save_creds, get_anon_cred

import google

def test_read_and_save_creds():
    creds = {"mocked":"credentials"}
    save_creds(creds)
    r_creds = read_creds()
    assert creds == r_creds

def test_get_anon_creds():
    with get_anon_cred() as cred:
        assert type(cred) == google.auth.credentials.AnonymousCredentials