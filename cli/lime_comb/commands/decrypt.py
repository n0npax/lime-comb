from dataclasses import dataclass

from lime_comb.commands.base import Command
from lime_comb.commands.common import add_message_parameters
from lime_comb.config import config
from lime_comb.gpg import decrypt


@dataclass
class DecryptCommand(Command):
    aliases: str = ("d", "dec")
    name: str = "decrypt"
    help: str = "Decrypt message"

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            self.name, aliases=self.aliases, help=self.help
        )
        add_message_parameters(self.parser)

    def __call__(self, msgs):
        for msg in msgs:
            decrypted_msg = decrypt(msg, always_trust=True, passphrase=config.password)
            yield decrypted_msg
