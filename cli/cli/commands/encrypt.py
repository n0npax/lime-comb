from dataclasses import dataclass
from cli.auth.google import get_anon_cred, get_cred
from cli.commands.base import Command, import_keys
from cli.commands.common import add_message_parameters, add_msg_merge, add_msg_recv
from cli.config import Config
from cli.gpg import encrypt, get_existing_pub_keys


@dataclass
class EncryptCommand(Command):
    aliases: str = ("e", "enc")
    name: str = "encrypt"
    help: str = """Encrypt message for receipment.
You can pass multiple messages by passing -m before earch message
Or -f before each file you want to encrypt"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            self.name, aliases=self.aliases, help=self.help
        )
        add_message_parameters(self.parser)
        add_msg_recv(self.parser)
        add_msg_merge(self.parser)

    def __call__(self, msgs, recipients, merge=False):
        if Config.always_import:
            with get_cred(Config.oauth_gcp_conf) as cred:
                # with get_anon_cred() as cred:
                for email in recipients:
                    import_keys(email, cred)
        for email in recipients:
            if not get_existing_pub_keys(email):
                import_keys(email, cred)
        if merge:
            msgs = ["\n---\n".join(msgs)]
        for msg in msgs:
            yield encrypt(recipients, msg)
