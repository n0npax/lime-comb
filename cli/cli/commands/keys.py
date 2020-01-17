from dataclasses import dataclass
from cli.gpg import geneate_keys, get_existing_priv_key
from cli.config import Config
from cli.commands.base import Command


@dataclass
class KeysCommand(Command):
    aliases: str = ("k", "keys")
    name: str = "keys"
    help: str = "keys management"

    def __call__(self, args):
        if args.command == "generate":
            print(geneate_keys())
        else:
            print(get_existing_priv_key())
