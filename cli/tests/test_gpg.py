import os
import tempfile

import pytest

from lime_comb.config import config
from lime_comb.gpg import (
    GPGException,
    decrypt,
    delete_gpg_key,
    encrypt,
    export_key,
    get_existing_priv_keys,
    get_existing_pub_keys,
    import_gpg_key,
)

from .conftest import keypair, pub_key


class TestGpg:
    def test_get_priv_key(self, mocker, username, password, keypair):
        keys = get_existing_priv_keys()
        assert keys
        for k in keys:
            assert len(k) >= 2

    def test_get_pub_key(self, mocker, username, password, keypair):
        keys = get_existing_pub_keys(config.email)
        assert keys
        for k in keys:
            assert len(k) >= 2

    def test_encrypt_ok(self, mocker, username, password, keypair):
        enc_msg = encrypt(config.email, "test data")
        assert enc_msg.startswith("-----BEGIN PGP MESSAGE----")

    def test_encrypt_invalid_email(self, mocker, username, password, keypair):
        with pytest.raises(GPGException):
            encrypt("not valid email", "test data")

    def test_decrypt_ok(self, mocker, username, password, keypair):
        input_data = "test_data"
        enc_msg = encrypt(config.email, input_data)
        dec_msg = decrypt(enc_msg)
        assert dec_msg == input_data

    def test_encrypt_invalid_data(self, mocker, username, password, keypair):
        with pytest.raises(GPGException):
            decrypt("invalid data")

    def test_generate_keypair(self, mocker, username, password, keypair):
        assert keypair

    def test_import_gpg_key_invalid_data(self, mocker, username, password, keypair):
        with pytest.raises(GPGException):
            for _ in import_gpg_key("invalid data"):
                pass

    def test_import_gpg_key_ok_data(self, mocker, username, password, pub_key):
        import_gpg_key(pub_key)

    def test_export_key(self, mocker, username, password, keypair):
        _, _, fingerprint = keypair
        assert export_key(fingerprint).startswith("-----BEGIN PGP")

    def test_delete_gpg_key(self, mocker, username, password, keypair):
        for k in delete_gpg_key(keypair, config.password):
            assert "ok" in k
