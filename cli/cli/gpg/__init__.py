import gnupg

from cli.config import Config

gpg = gnupg.GPG(gnupghome=str(Config.keyring_dir), keyring=Config.app_name)
gpg.encoding = "utf-8"


def encrypt(emails, data):
    encrypted_data = gpg.encrypt(data, emails, always_trust=True, sign=False)
    if not encrypted_data.ok:
        raise Exception(f"encryption failed {encrypted_data.stderr}")
    return str(encrypted_data)


def geneate_keys():
    key_input = gpg.gen_key_input(
        key_type="ECDSA",
        key_length=4096,
        name_real=Config.username,
        name_email=Config.email,
        name_comment=Config.comment,
        passphrase=Config.password,
    )
    return gpg.gen_key(key_input)

def get_local_pub_key(email):
    pub_keys = gpg.list_keys()
    for k, v in pub_keys.key_map.items():
        if v["uids"] == [f"{Config.username} ({Config.comment}) <{Config.email}>"]:
            return k

def get_existing_priv_key():
    private_keys = gpg.list_keys(True)
    for k, v in private_keys.key_map.items():
        if v["uids"] == [f"{Config.username} ({Config.comment}) <{Config.email}>"]:
            return k

def get_priv_key():
    existing_priv_key = get_existing_priv_key()
    if existing_priv_key:
        return existing_priv_key
    return get_priv_key()


def import_pub_key(data):
    status = gpg.import_keys(data)
    for r in status.results:
        if not r['fingerprint']:
            raise Exception(f"key import error: {r}")