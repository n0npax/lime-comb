import os

import gnupg
from cli.config import Config

GPGHOME = str(Config.keyring_dir)
KEYRING = None  # f"{GPGHOME}/../keyring-"+Config.app_name
SECRET_KEYRING = None  # f"{KEYRING}-secrets"
gpg = gnupg.GPG(
    gnupghome=GPGHOME,
    keyring=KEYRING,
    use_agent=True,
    verbose=False,
    secret_keyring=SECRET_KEYRING,
)
gpg.encoding = "utf-8"


def decrypt(data, *args, **kwargs):
    decrypted_data = gpg.decrypt(
        data, extra_args=["--no-default-keyring"], passphrase=Config.password
    )
    if not decrypted_data.ok:
        err = getattr(decrypted_data, "stderr", "expected stderr not found")
        raise Exception(f"decryption failed {err}")
    return str(decrypted_data)


def encrypt(emails, data):
    encrypted_data = gpg.encrypt(data, emails, always_trust=True, sign=False)
    if not encrypted_data.ok:
        err = getattr(encrypted_data, "stderr", "expected stderr not found")
        raise Exception(f"encryption failed {err}")
    return str(encrypted_data)


def geneate_keys():
    key_input = gpg.gen_key_input(
        key_type="RSA",
        key_length=4096,
        name_real=Config.username,
        name_email=Config.email,
        name_comment=Config.comment,
        passphrase=Config.password,
    )
    return gpg.gen_key(key_input)


def get_existing_pub_keys(email=None):
    yield from get_existing_keys(email=None, priv=False)


def get_existing_keys(email=None, priv=False):
    if not email:
        email = Config.email
    pub_keys = gpg.list_keys(priv)
    for k, v in pub_keys.key_map.items():
        if email in v["uids"][0]:
            yield (k, v["uids"])


def get_existing_priv_keys():
    yield from get_existing_keys(email=None, priv=True)


def import_gpg_key(data):
    status = gpg.import_keys(data)
    for r in status.results:
        if not r["fingerprint"]:
            raise Exception(f"key import error: {r}")
        yield r


def delete_gpg_key(fingerprint, passphrase):
    yield "priv", str(
        gpg.delete_keys(fingerprint, secret=bool(passphrase), passphrase=passphrase)
    )
    yield "pub", str(gpg.delete_keys(fingerprint))


def export_key(keyids, priv=False):
    return gpg.export_keys(keyids, secret=priv, passphrase=Config.password)
