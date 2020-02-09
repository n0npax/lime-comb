from dataclasses import dataclass

from cli.commands.base import Command
from cli.config import Config
from cli.gpg import (
    geneate_keys,
    get_existing_priv_keys,
    get_existing_pub_keys,
    export_key,
)


@dataclass
class KeysCommand(Command):
    aliases: str = ("k", "keys")
    name: str = "keys"
    help: str = "keys management"
    choices: tuple = ("generate", "list", "push", "pull")

    def __call__(self, args):
        if args.command == "generate":
            yield geneate_keys()
        elif args.command == "list":
            yield from get_existing_priv_keys()
        elif args.command == "push":
            print("TODO implement Me keys upload")
            for k in get_existing_priv_keys():
                key_id = k[0]
                priv_key = export_key(key_id, True)
        else:
            raise Exception("not supported subcommands")
