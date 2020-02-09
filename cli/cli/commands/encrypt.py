from dataclasses import dataclass

from cli.auth.google import get_anon_cred
from cli.commands.base import Command
from cli.config import Config
from cli.firestore.fetch import get_gpg
from cli.gpg import encrypt, get_existing_pub_keys, import_pub_key


@dataclass
class EncryptCommand(Command):
    aliases: str = ("e", "enc")
    name: str = "encrypt"
    help: str = "Encrypt message for receipment. You can pass multiple messages by passing -m before earch message"

    def __call__(self, msgs, recipients, merge=False):
        if Config.always_import:
            with get_anon_cred() as cred:
                for email in recipients:
                    self._import_key(email, cred)
        for email in recipients:
            if not get_existing_pub_keys(email):
                self._import_key(email, cred)
        if merge:
            msgs = ["\n---\n".join(msgs)]
        for msg in msgs:
            yield encrypt(recipients, msg)

    def _import_key(self, email, cred):
        key_str = get_gpg(cred, email)
        import_pub_key(key_str)
