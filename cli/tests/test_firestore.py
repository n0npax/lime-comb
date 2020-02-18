import random
from uuid import uuid4

import google
import grpc
import pytest
from google.cloud.firestore_v1.types import Document, Value

import cli
from cli.auth.google import get_anon_cred
from cli.config import Config
from cli.firestore import database

from .conftest import cred


@pytest.fixture
def collection_id():
    return "existingTestCollection"


@pytest.fixture
def document_id():
    return str(uuid4())


@pytest.fixture
def firestore_parent():
    return "projects/lime-comb/databases/(default)/documents"


@pytest.fixture
def document():
    return Document(fields={"senseOfLife": Value(integer_value=42)})


@pytest.yield_fixture
def local_firestore(
    mocker, cred, document, collection_id, firestore_parent, document_id
):
    Config.firestore_target = "localhost:8080"
    f = lambda _: grpc.insecure_channel(Config.firestore_target)
    old_f = cli.firestore.database._create_channel
    cli.firestore.database._create_channel = f
    mocker_document = cli.firestore.database.put_document(
        cred,
        firestore_parent,
        collection_id,
        document=document,
        document_id=document_id,
    )
    doc_name = f"{firestore_parent}/{collection_id}/{document_id}"
    yield mocker_document
    cli.firestore.database.delete_document(cred, doc_name)
    cli.firestore.database._create_channel = old_f


def test_decodebase64():
    foo_encoded = "Zm9vCg=="
    assert "foo\n" == database._decode_base64(foo_encoded)


def test_get_doc(local_firestore, firestore_parent, collection_id, document_id):
    cli.firestore.database.get_document(
        cred, firestore_parent + f"/{collection_id}/{document_id}"
    )
