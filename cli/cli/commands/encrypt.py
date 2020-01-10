from dataclasses import dataclass

from cli.commands.base import Command
from cli.auth.google import get_anon_cred
from cli.firestore.fetch import get_gpg
from cli.gpg import get_local_pub_key, import_pub_key, encrypt
from cli.config import Config


@dataclass
class EncryptCommand(Command):
    aliases: str = ("e", "enc")
    name: str = "encrypt"
    help: str = "encrypt message for receipment"
    pass

    def __call__(self, msgs, recipients):
        if Config.always_import:
            with get_anon_cred() as cred:
                for email in recipients:
                    self._import_key(email, cred)
        for email in recipients:
            if not get_local_pub_key(email):
                self._import_key(email, cred)
        msgs = "\n---\n".join(msgs)
        encrypted_msgs = encrypt(recipients, msgs)
        print(encrypted_msgs)

    def _import_key(self, email, cred):
        key_str = get_gpg(cred, email)
        import_pub_key(key_str)
