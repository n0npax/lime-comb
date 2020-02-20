import random
from uuid import uuid4

import google
import grpc
import pytest
from google.cloud.firestore_v1.types import Document, Value
from mockfirestore.client import MockFirestore

import cli
from cli.auth.google import get_anon_cred
from cli.config import Config
from cli.firestore import database

from .conftest import *


def test_encode_decodebase64():
    foo = "foo"
    foo_encoded = database._encode_base64(foo)
    assert foo_encoded == "Zm9v"
    assert foo == database._decode_base64(foo_encoded)


@pytest.yield_fixture
def mocked_db(key_id):
    mock_db = MockFirestore()
    cli.firestore.database.list_gpg_ids = fake_list_gpg_ids(key_id)
    cli.firestore.database.get_firestore_db = lambda _: mock_db
    yield mock_db
    mock_db.reset()


def fake_list_gpg_ids(key_id):
    def list_gpg_ids(*args, **kwargs):
        yield key_id

    return list_gpg_ids


@pytest.yield_fixture
def mocked_gpg_key(mocked_db, key_id, email, domain, priv_key, pub_key):
    mocked_db.collection(domain).document(f"{email}/{key_id}/priv").set(
        {"data": priv_key}
    )
    mocked_db.collection(domain).document(f"{email}/{key_id}/pub").set(
        {"data": pub_key}
    )
    yield


def test_get_gpg_pub(mocked_gpg_key, email, pub_key, cred):
    keys = list(database.get_gpgs(cred, email))
    assert len(keys) > 0
    assert keys[0] == pub_key


def test_get_gpg_priv(mocked_gpg_key, email, priv_key, cred):
    keys = list(database.get_gpgs(cred, email, key_type="priv"))
    assert len(keys) > 0
    assert keys[0] == priv_key


def test_put_gpg_priv(mocked_db, cred, email, key_id, priv_key):

    database.put_gpg(cred, email, priv_key, key_id, key_type="priv")
    rec_priv_key = database.get_gpg(cred, email, key_id, key_type="priv")
    assert rec_priv_key == priv_key
