import tempfile
from pathlib import Path
from unittest.mock import PropertyMock, patch
from uuid import uuid4

import lime_comb
import lime_comb.config
import lime_comb.firestore.database
import pyperclip
import pytest
import requests_mock
from lime_comb.auth.google import get_anon_cred
from lime_comb.gpg import delete_gpg_key, geneate_keys
from mockfirestore.client import MockFirestore
from yaml import dump


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c


@pytest.fixture
def domain():
    return "example.com"


@pytest.fixture
def mocked_resp():
    return '{"some": "response"}'


@pytest.yield_fixture
def oauth_gcp_conf(mocked_resp, oauth_client_config):
    with requests_mock.Mocker(real_http=True) as m:
        m.register_uri(
            "GET", lime_comb.config.config.client_lime_comb_url, text=mocked_resp
        )
        yield


@pytest.yield_fixture
def temp_file():
    with tempfile.NamedTemporaryFile() as fp:
        yield fp


@pytest.fixture
def key_id(uuid):
    return uuid


@pytest.fixture
def uuid():
    return uuid4()


class Creds:
    def __init__(self, uuid, expired=True):
        self.expired = expired
        self.uuid = uuid


@pytest.fixture
def valid_cred(uuid):
    return Creds(expired=False, uuid=uuid)


@pytest.yield_fixture(autouse=True)
def credentials_file(mocker, config_file, uuid):
    path = Path(f"{lime_comb.config.config.credentials_file}.test-{uuid}")
    with patch(
        "lime_comb.config.Config.credentials_file", new_callable=PropertyMock
    ) as credentials_file_mock:
        credentials_file_mock.return_value = path
        yield


@pytest.yield_fixture(autouse=True)
def oauth_client_config(mocker, config_file, uuid):
    path = Path(f"{lime_comb.config.config.oauth_client_config}.test-{uuid}")
    with patch(
        "lime_comb.config.Config.oauth_client_config", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = path
        yield


@pytest.yield_fixture(autouse=True)
def email(mocker, config_file):
    _email = "example.example@example.com"
    with patch(
        "lime_comb.config.Config.email", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = _email
        yield _email


@pytest.yield_fixture(autouse=True)
def config_dir(mocker, config_file):
    with tempfile.TemporaryDirectory() as dir_name:
        mocker.PropertyMock(
            lime_comb.config.Config, "config_dir", return_value=Path(dir_name)
        )
        yield


@pytest.yield_fixture(autouse=True)
def no_cred(mocker, credentials_file):
    mocker.PropertyMock(
        lime_comb.config.Config, "credentials_file", return_value=Path("/dev/null")
    )
    yield


@pytest.yield_fixture(autouse=True)
def config_file(mocker, temp_file):
    PropertyMock(
        lime_comb.config.Config, "config_file", return_value=Path(temp_file.name)
    )
    yield temp_file.name


@pytest.fixture
def existing_config(config_file, email):
    with open(config_file, "w") as f:
        f.write(dump({"email": email}))


# TODO fix all mocks to use mocker
@pytest.yield_fixture(autouse=True)
def password(mocker, config_file):
    with patch(
        "lime_comb.config.Config.password", new_callable=PropertyMock
    ) as password_mock:
        password_mock.return_value = "dupa.8Polska12"
        yield


@pytest.fixture
def invalid_cred(uuid):
    return Creds(uuid=uuid)


@pytest.yield_fixture()
def pyperclip_copy(mocker):
    mocker.patch.object(pyperclip, "copy")
    yield


@pytest.yield_fixture
def web_login(mocker, uuid):
    mocker.patch.object(
        lime_comb.auth.google, "web_login", return_value=Creds(expired=False, uuid=uuid)
    )
    yield


def fake_list_gpg_ids(key_id):
    def list_gpg_ids(*args, **kwargs):
        yield key_id

    return list_gpg_ids


@pytest.yield_fixture()
def mocked_db(key_id, valid_cred, mocker):
    db = MockFirestore()
    mocker.patch.object(
        lime_comb.firestore.database, "get_firestore_db", return_value=db
    )
    mocker.patch.object(
        lime_comb.firestore.database,
        "list_gpg_ids",
        return_value=fake_list_gpg_ids(key_id)(),
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
    yield f"{key_id}"


@pytest.yield_fixture
def keypair():
    keys = geneate_keys()
    yield keys.fingerprint
    delete_gpg_key(keys.fingerprint, lime_comb.config.config.password)


@pytest.fixture
def priv_key():
    return """-----BEGIN PGP PRIVATE KEY BLOCK-----

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
Fs77nmd7O6cSw28=
=ezAo
-----END PGP PRIVATE KEY BLOCK-----
"""


@pytest.fixture
def pub_key():
    return """-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=JSru
-----END PGP PUBLIC KEY BLOCK-----
"""
