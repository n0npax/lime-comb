import pytest

from cli.firestore import fetch
from cli.auth.google import get_anon_cred
from cli.config import Config
from .conftest import cred
import grpc
import cli
import google

from google.cloud.firestore_v1.types import Document, Value

@pytest.fixture
def collection_id():
    return "testExist"


@pytest.fixture
def firestore_parent():
    return "projects/lime-comb/databases/(default)/documents"


@pytest.fixture
def document():
    return Document(fields={'Field1': Value(integer_value=44)})


@pytest.yield_fixture
def local_firestore(mocker, cred, document, collection_id, firestore_parent):
    Config.firestore_target = "localhost:5004"
    f = lambda _: grpc.insecure_channel(Config.firestore_target)
    old_f = cli.firestore.fetch._create_channel
    cli.firestore.fetch._create_channel = f
    print(document)
    a = cli.firestore.fetch.put_document(
        cred, firestore_parent, collection_id, document=document, document_id=None
    )
    print(a)
    yield
    cli.firestore.fetch._create_channel = old_f


def test_decodebase64():
    foo_encoded = "Zm9vCg=="
    assert "foo\n" == fetch._decode_base64(foo_encoded)


def test_get_doc(local_firestore,firestore_parent):
    print(cli.firestore.fetch.get_document(cred, firestore_parent+"/sa/T0dzr7zx4ceGkVzbcuGF"))
