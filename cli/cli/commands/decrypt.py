from dataclasses import dataclass

from cli.commands.base import Command
from cli.commands.common import add_message_parameters
from cli.config import Config
from cli.gpg import decrypt


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
            decrypted_msg = decrypt(msg, always_trust=True, passphrase=Config.password)
            yield decrypted_msg
