from dataclasses import dataclass

from cli.commands.base import Command
from cli.auth.google import get_anon_cred
from cli.firestore.fetch import get_gpg
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
                    print(get_gpg(cred, email)) #TODO import
