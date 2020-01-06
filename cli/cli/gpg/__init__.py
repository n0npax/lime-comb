import gnupg

gpg = gnupg.GPG(gnupghome=None)
gpg.encoding = "utf-8"


def encrypt(emails, data):
    encrypted_data = gpg.encrypt(data, emails)
    if not encrypted_data.ok:
        raise Exception("encryption failed {encrypted_data.stderr}")
    return str(encrypted_data)
