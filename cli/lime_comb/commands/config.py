from dataclasses import dataclass

from email_validator import EmailSyntaxError

from lime_comb.commands.base import Command
from lime_comb.config import config
from lime_comb.logger.logger import logger


@dataclass
class ConfigCommand(Command):
    aliases: str = ("c", "conf", "config")
    name: str = "config"
    help: str = "config management"
    choices: tuple = ("get", "set", "list", "generate", "regenerate")

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            self.name, aliases=self.aliases, help=self.help
        )
        self.parser.add_argument("command", choices=self.choices, help=self.help)
        self.parser.add_argument("name", nargs="?", help="property name")
        self.parser.add_argument("value", nargs="?", help="property value")

    def __call__(self, args):
        name, value = args.name, args.value
        if args.command == "list":
            for k, v in config.get_configurable().items():
                yield (k, v)
        elif args.command in ("generate", "regenerate"):
            config._gen_config()
        elif args.command == "set":
            try:
                getattr(config, name)
                setattr(config, name, value)
                yield (name, value)
            except AttributeError:
                logger.error(f"'{name}' is not valid property")
            except EmailSyntaxError as e:
                logger.error(e)
        elif args.command == "get":
            try:
                yield name, getattr(config, name)
            except AttributeError:
                logger.error(f"'{name}' is not valid property")
        else:
            raise Exception("not supported subcommands")
