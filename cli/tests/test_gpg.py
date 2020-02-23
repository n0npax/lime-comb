import os
import tempfile

import pytest
from lime_comb_cli.config import Config
from lime_comb_cli.gpg import (GPGException, decrypt, delete_gpg_key, encrypt,
                               export_key, geneate_keys,
                               get_existing_priv_keys, get_existing_pub_keys,
                               import_gpg_key)

from .conftest import public_key_string


@pytest.yield_fixture
def keypair():
    keys = geneate_keys()
    yield keys.fingerprint
    delete_gpg_key(keys.fingerprint, Config.password)


class TestGpg:
    def test_get_priv_key(self, keypair):
        keys = get_existing_priv_keys()
        assert keys
        for k in keys:
            assert len(k) >= 2

    def test_get_pub_key(self, keypair):
        keys = get_existing_pub_keys(Config.email)
        assert keys
        for k in keys:
            assert len(k) >= 2

    def test_encrypt_ok(self, keypair):
        enc_msg = encrypt(Config.email, "test data")
        assert enc_msg.startswith("-----BEGIN PGP MESSAGE----")

    def test_encrypt_invalid_email(self, keypair):
        with pytest.raises(GPGException):
            encrypt("not valid email", "test data")

    def test_decrypt_ok(self, keypair):
        input_data = "test_data"
        enc_msg = encrypt(Config.email, input_data)
        dec_msg = decrypt(enc_msg)
        assert dec_msg == input_data

    def test_encrypt_invalid_data(self, keypair):
        with pytest.raises(GPGException):
            decrypt("invalid data")

    def test_generate_keypair(self, keypair):
        assert keypair

    def test_delete_gpg_key(self, keypair):
        for k in delete_gpg_key(keypair, Config.password):
            assert "ok" in k

    def test_import_gpg_key_invalid_data(self):
        with pytest.raises(GPGException):
            for _ in import_gpg_key("invalid data"):
                pass

    def test_import_gpg_key_ok_data(self, public_key_string):
        import_gpg_key(public_key_string)

    def test_export_key(self, keypair):
        assert export_key(keypair).startswith("-----BEGIN PGP")
