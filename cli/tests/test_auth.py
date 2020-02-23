import os
import tempfile
from uuid import uuid4

import google
import pytest
from google.auth.credentials import AnonymousCredentials

import lime_comb.auth.google
from lime_comb.auth.google import (get_anon_cred, get_cred, read_creds,
                                       save_creds)
from lime_comb.config import Config

from .conftest import *


class TestAuth:
    def test_read_and_save_creds(self, valid_cred):
        save_creds(valid_cred)
        r_creds = read_creds()
        assert valid_cred.uuid == r_creds.uuid

    def test_get_saved_creds(self, valid_cred):
        save_creds(valid_cred)
        with get_cred(Config.credentials_file) as cred:
            assert not cred.expired

    def test_get_saved_expired_creds(self, invalid_cred, web_login):
        save_creds(invalid_cred)
        with get_cred(Config.credentials_file) as cred:
            assert not cred.expired

    def test_get_no_saved_creds(self, no_cred, web_login):
        with get_cred(Config.credentials_file) as cred:
            assert not cred.expired

    def test_get_anon_creds(self):
        with get_anon_cred() as cred:
            assert type(cred) == AnonymousCredentials
