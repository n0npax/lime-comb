import os
import tempfile

import pytest

from cli.config import Config
from cli.gpg import (
    encrypt,
    geneate_keys,
    decrypt,
    get_existing_priv_keys,
    get_existing_pub_keys,
    delete_gpg_key,
)


@pytest.yield_fixture
def keypair():
    keys = geneate_keys()
    yield keys.fingerprint
    delete_gpg_key(keys.fingerprint, Config.password)


def test_get_priv_key(keypair):
    keys = get_existing_priv_keys()
    assert keys
    for k in keys:
        assert len(k) >= 2


def test_get_pub_key(keypair):
    keys = get_existing_pub_keys(Config.email)
    assert keys
    for k in keys:
        assert len(k) >= 2


def test_encrypt(keypair):
    enc_msg = encrypt(Config.email, "test data")
    assert enc_msg.startswith("-----BEGIN PGP MESSAGE----")


def test_decrypt(keypair):
    input_data = "test_data"
    enc_msg = encrypt(Config.email, input_data)
    dec_msg = decrypt(enc_msg)
    assert dec_msg == input_data


def test_generate_keypair(keypair):
    assert keypair


def test_delete_gpg_key(keypair):
    for k in delete_gpg_key(keypair, Config.password):
        assert "ok" in k
