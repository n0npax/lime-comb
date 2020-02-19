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


def test_encode_decodebase64():
    foo = "foo"
    foo_encoded = database._encode_base64(foo)
    assert foo_encoded == "Zm9v"
    assert foo == database._decode_base64(foo_encoded)
