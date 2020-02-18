import os
import tempfile

import pytest

from cli.config import Config
from cli.gpg import encrypt, geneate_keys, decrypt


@pytest.yield_fixture(autouse=True)
def temp_data_dir():
    data_dir = tempfile.mkdtemp()
    Config.data_dir = data_dir
    yield data_dir
    os.rmdir(data_dir)


@pytest.fixture
def keypair(temp_data_dir):
    keys = geneate_keys()
    return keys.fingerprint


def test_encrypt(keypair):
    enc_msg = encrypt(Config.email, "test data")
    assert enc_msg.startswith("-----BEGIN PGP MESSAGE----")


def test_decrypt(keypair):
    input_data = "test_data"
    enc_msg = encrypt(Config.email, input_data)
    dec_msg = decrypt(enc_msg)
    assert dec_msg == input_data

def test_generate_keypair():
    keys = geneate_keys()
    assert keys.fingerprint
