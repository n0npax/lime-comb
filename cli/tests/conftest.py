from uuid import uuid4

import pytest
from mockfirestore.client import MockFirestore

import cli
import cli.firestore.database
from cli.auth.google import get_anon_cred
from cli.config import Config


@pytest.fixture
def public_key_string():
    return """-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=+u6b
-----END PGP PUBLIC KEY BLOCK-----"""


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
