"""
from mockfirestore.client import MockFirestore
import pytest


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
"""
