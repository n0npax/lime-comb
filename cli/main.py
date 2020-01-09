#!/usr/bin/env python3
import argparse
import logging
import os
import sys

import email_validator

import cli
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
)

enc_parsers = subparsers.add_parser(
    "encrypt", aliases=["enc", "e"], help="encrypt message for receipment"
)
dec_parsers = subparsers.add_parser(
    "decrypt", aliases=["dec", "d"], help="decrypt message"
)
config_parsers = subparsers.add_parser(
    "config", aliases=["conf", "c"], help="configuration"
)
keys_parsers = subparsers.add_parser("keys", aliases=["k"], help="keys management")

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
    p.set_defaults(command_name=lambda: name)


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


def get_message():
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
    command_name = args.command_name()

    if command_name == "dec":
        pass
    if command_name == "enc":
        pass

    from cli.auth.google import get_cred
    from cli.firestore.fetch import get_gpg
    from cli.config import OAUTH_GCP_CONF

    with get_cred(OAUTH_GCP_CONF) as cred:
        print(get_gpg(cred, "marcin.niemira@gmail.com"))
