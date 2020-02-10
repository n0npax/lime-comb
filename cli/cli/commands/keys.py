from dataclasses import dataclass

from cli.auth.google import get_anon_cred, get_cred
from cli.commands.base import Command
from cli.config import Config
from cli.firestore.fetch import get_gpg, put_gpg
from cli.gpg import (export_key, geneate_keys, get_existing_priv_keys,
                     get_existing_pub_keys)


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
        elif args.command == "pull":
            email = Config.email
            with get_cred(Config.oauth_gcp_conf) as cred:
                priv = get_gpg(cred, email, key_type="priv")
                pub = get_gpg(cred, email, key_type="pub")
                print(priv)
                # TODO import to keyring
        elif args.command == "push":
            email = Config.email
            with get_cred(Config.oauth_gcp_conf) as cred:
                for k in get_existing_priv_keys():
                    key_id = k[0]
                    priv_key = export_key(key_id, True)
                    put_gpg(cred, email, priv_key, key_type="priv", key_name=key_id)
                for k in get_existing_pub_keys(Config.email):
                    key_id = k[0]
                    pub_key = export_key(key_id, False)
                    put_gpg(cred, email, pub_key, key_type="pub", key_name=key_id)
        else:
            raise Exception("not supported subcommands")
