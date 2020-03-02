from dataclasses import dataclass

import lime_comb.firestore.database as database
from lime_comb.auth.google import get_cred
from lime_comb.commands.base import Command
from lime_comb.config import config
from lime_comb.gpg import (
    delete_gpg_key,
    export_key,
    geneate_keys,
    get_existing_priv_keys,
    get_existing_pub_keys,
    import_gpg_key,
)


@dataclass
class KeysCommand(Command):
    aliases: str = ("k", "keys")
    name: str = "keys"
    help: str = "keys management"
    choices: tuple = ("generate", "list-priv", "list-pub", "push", "pull", "delete")

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            self.name, aliases=self.aliases, help=self.help
        )
        self.parser.add_argument("command", choices=self.choices, help=self.help)
        self.parser.add_argument("argument", nargs="?", help="ID filter (optional)")

    def __call__(self, args):

        email = config.email

        if args.command == "generate":
            yield [geneate_keys()]
        elif args.command == "delete":
            with get_cred(config.oauth_gcp_conf) as cred:
                yield from delete_gpg_key(args.argument, config.password)
                database.delete_gpg(cred, email, args.argument)
        elif args.command == "list-pub":
            yield from get_existing_pub_keys(args.argument)
        elif args.command == "list-priv":
            yield from get_existing_priv_keys()
        elif args.command == "pull":
            with get_cred(config.oauth_gcp_conf) as cred:
                if args.argument:
                    email = args.argument
                privs = database.get_gpgs(cred, email, key_type="priv")
                pubs = database.get_gpgs(cred, email, key_type="pub")
                for p in privs:
                    yield from import_gpg_key(p)
                for p in pubs:
                    yield from import_gpg_key(p)
        elif args.command == "push":
            if not config.export_priv_key:
                yield [
                    "configuration denies pushing priv key. Please update config first"
                ]
            password = None
            if config.export_password:
                password = config.password
                yield ["exporting password with key"]
            email = config.email
            with get_cred(config.oauth_gcp_conf) as cred:
                for k in get_existing_priv_keys():
                    key_id = k[0]
                    priv_key = export_key(key_id, True)
                    database.put_gpg(
                        cred,
                        email,
                        priv_key,
                        key_type="priv",
                        key_name=key_id,
                        password=password,
                    )
                    yield key_id, email
                for k in get_existing_pub_keys(config.email):
                    key_id = k[0]
                    pub_key = export_key(key_id, False)
                    database.put_gpg(
                        cred, email, pub_key, key_type="pub", key_name=key_id
                    )
                    yield key_id, email

        else:
            raise Exception("not supported subcommands")
