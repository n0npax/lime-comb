from cli.commands.base import Command
from dataclasses import dataclass


@dataclass
class EncryptCommand(Command):
    aliases: str = ("e", "enc")
    name: str = "encrypt"
    help: str = "encrypt message for receipment"
    pass
