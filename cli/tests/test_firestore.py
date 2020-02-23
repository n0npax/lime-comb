import random
from uuid import uuid4

import google
import grpc
import pytest
from google.cloud.firestore_v1.types import Document, Value

import lime_comb_cli
from lime_comb_cli.auth.google import get_anon_cred
from lime_comb_cli.config import Config
from lime_comb_cli.firestore import database

from .conftest import *


class TestDatabse:
    def test_encode_decodebase64(self):
        foo = "foo"
        foo_encoded = database._encode_base64(foo)
        assert foo_encoded == "Zm9v"
        assert foo == database._decode_base64(foo_encoded)

    def test_get_gpg_pub(self, mocked_gpg_key, email, pub_key, cred):
        keys = list(database.get_gpgs(cred, email))
        assert len(keys) > 0
        assert keys[0] == pub_key

    def test_get_gpg_priv(self, mocked_gpg_key, email, priv_key, cred):
        keys = list(database.get_gpgs(cred, email, key_type="priv"))
        assert len(keys) > 0
        assert keys[0] == priv_key

    def test_put_gpg_priv(self, mocked_db, cred, email, key_id, priv_key):
        database.put_gpg(cred, email, priv_key, key_id, key_type="priv")
        rec_priv_key = database.get_gpg(cred, email, key_id, key_type="priv")
        assert rec_priv_key == priv_key

    def test_delete_gpg(self, mocked_db, cred, email, key_id, priv_key):
        database.put_gpg(cred, email, priv_key, key_id, key_type="priv")
        database.delete_gpg(cred, email, key_id, key_type="priv")
        rec_priv_key = database.get_gpg(cred, email, key_id, key_type="priv")
        assert rec_priv_key == None
