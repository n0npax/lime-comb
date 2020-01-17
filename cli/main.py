#!/usr/bin/env python3
import argparse
import logging
import os
import sys

import email_validator

import cli
from cli.commands.decrypt import DecryptCommand
from cli.commands.encrypt import EncryptCommand
from cli.commands.keys import KeysCommand
from cli.logger.logger import logger


def validate_filepath(fp):
    if not os.path.isfile(fp):
        raise argparse.ArgumentTypeError(f"have to be file")
    return fp


def validate_email(email):
    email_validator.validate_email(email)
    return email


parser = argparse.ArgumentParser(description="lime comb tool.")

parser.add_argument(
    "--version",
    dest="version",
    required=False,
    action="store_true",
    help="show current version",
)
parser.add_argument(
    "--log-lvl",
    dest="log_lvl",
    required=False,
    default="WARNING",
    action="store",
    choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
    help="log level",
)

subparsers = parser.add_subparsers(
    help="use --help to check help for sub-command",
    title="commands",
    description="Top level supported commands",
    required=True,
    dest="top_command",
)

enc_cmd = EncryptCommand()
enc_parsers = subparsers.add_parser(
    enc_cmd.name, aliases=enc_cmd.aliases, help=enc_cmd.help
)
dec_cmd = DecryptCommand()

dec_parsers = subparsers.add_parser(
    dec_cmd.name, aliases=dec_cmd.aliases, help=dec_cmd.help
)

enc_parsers.add_argument(
    "-t",
    "--to",
    dest="receipments",
    required=False,
    action="append",
    default=[],
    help="receipment of the message",
    type=validate_email,
)
enc_parsers.add_argument(
    "--merge-messages",
    "--mm",
    dest="merge_messages",
    required=False,
    action="store_true",
    default=False,
    help="merge multile messages into 1",
)
for name, p in {"enc": enc_parsers, "dec": dec_parsers}.items():
    p.add_argument(
        "-f",
        "--file",
        dest="files",
        required=False,
        action="append",
        help="file",
        default=[],
        type=validate_filepath,
    )
    p.add_argument(
        "-m",
        "--message",
        dest="messages",
        required=False,
        action="append",
        help="message",
        default=[],
    )


# TODO provide class for config and keys
config_parsers = subparsers.add_parser(
    "config", aliases=["conf", "c"], help="configuration"
)
keys_cmd = KeysCommand()
keys_parsers = subparsers.add_parser(
    keys_cmd.name, aliases=keys_cmd.aliases, help=keys_cmd.help
)
keys_parsers.add_argument("command", choices=["generate", "list"], help="main command")


def parse_common():
    logger.setLevel(args.log_lvl)

    logger.info(f"log lvl {logger.getEffectiveLevel()}")
    if args.version:
        print(f"version: {cli.__version__}")
        sys.exit(0)


def get_receipments():
    if not args.receipments:
        logger.info("No receipmens. Asking userto type in")
        args.receipments = input("please specify receipments(space separated)\n")
    return args.receipmens


def get_message(args):
    if args.files:
        for fn in args.files:
            logger.debug(f"adding content of {fn} to messages")
            with open(fn, "r") as f:
                args.messages.append(f.read())
    if not args.messages:
        logger.warning("no message to encrypt")
        print("No message to encrypt")
        sys.exit(1)
    return args.messages


args = parser.parse_args(sys.argv[1:])
if __name__ == "__main__":
    parse_common()

    if args.top_command in dec_cmd.aliases:
        for m in dec_cmd(get_message(args)):
            print(m)
    if args.top_command in enc_cmd.aliases:
        for m in enc_cmd(get_message(args), args.receipments, merge=args.merge_messages):
            print(m)
    if args.top_command in keys_cmd.aliases:
        keys_cmd(args)
