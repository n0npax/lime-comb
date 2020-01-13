from dataclasses import dataclass

from cli.commands.base import Command


@dataclass
class DecryptCommand(Command):
    aliases: str = ("d", "dec")
    name: str = "decrypt"
    help: str = "decrypt message"
    
    def __call__(self):
        pass
