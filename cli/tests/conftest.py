from uuid import uuid4

import pytest
from mockfirestore.client import MockFirestore

import cli
import cli.firestore.database
from cli.auth.google import get_anon_cred
from cli.config import Config


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c


@pytest.fixture
def domain():
    return "example.com"


@pytest.fixture
def email():
    return "jan.twardowski@example.com"


@pytest.fixture
def key_id():
    return uuid4()


@pytest.fixture
def priv_key():
    return "priv key data"


@pytest.fixture
def pub_key():
    return "pub key data"


class Creds:
    def __init__(self, expired=True):
        self.expired = expired
        self.uuid = uuid4()


@pytest.fixture
def valid_cred():
    return Creds(expired=False)


@pytest.yield_fixture
def no_cred():
    cli.config.Config.credentials_file = "/dev/null"
    yield


@pytest.fixture
def invalid_cred():
    return Creds()


@pytest.yield_fixture
def web_login(mocker):
    mocker.patch.object(cli.auth.google, "web_login", return_value=Creds(expired=False))
    yield


def fake_list_gpg_ids(key_id):
    def list_gpg_ids(*args, **kwargs):
        yield key_id

    return list_gpg_ids


@pytest.yield_fixture
def mocked_db(key_id, valid_cred, mocker):
    db = MockFirestore()
    mocker.patch.object(cli.firestore.database, "get_firestore_db", return_value=db)
    mocker.patch.object(
        cli.firestore.database, "list_gpg_ids", return_value=fake_list_gpg_ids(key_id)()
    )
    yield db
    db.reset()


@pytest.yield_fixture
def mocked_gpg_key(mocked_db, key_id, email, domain, priv_key, pub_key):
    mocked_db.collection(domain).document(f"{email}/{key_id}/priv").set(
        {"data": priv_key}
    )
    mocked_db.collection(domain).document(f"{email}/{key_id}/pub").set(
        {"data": pub_key}
    )
