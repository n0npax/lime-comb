from cli.commands.base import Command
from dataclasses import dataclass


@dataclass
class DecryptCommand(Command):
    aliases: str = ("d", "dec")
    name: str = "decrypt"
    help: str = "decrypt message"
    pass
