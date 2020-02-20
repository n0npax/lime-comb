#!/usr/bin/env python3
import argparse
import logging
import os
import sys

import pyperclip
from tabulate import tabulate
from tqdm import tqdm

import cli
from cli.commands.base import validate_email, validate_filepath
from cli.commands.decrypt import DecryptCommand
from cli.commands.encrypt import EncryptCommand
from cli.commands.keys import KeysCommand
from cli.logger.logger import logger

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

keys_cmd = KeysCommand(subparsers)

enc_cmd = EncryptCommand(subparsers)

dec_cmd = DecryptCommand(subparsers)

# TODO provide class for config and keys


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
        logger.warning("No message to encrypt")
        sys.exit(1)
    return args.messages


args = parser.parse_args(sys.argv[1:])
if __name__ == "__main__":
    parse_common()

    if args.top_command in dec_cmd.aliases:
        decrypted = []
        for m in tqdm(dec_cmd(get_message(args)), desc="decrypting"):
            decrypted.append(m)
        decrypted = "\n---\n".join(decrypted)
        pyperclip.copy(decrypted)
        print(decrypted)

    if args.top_command in enc_cmd.aliases:
        encrypted = []
        for m in tqdm(
            enc_cmd(get_message(args), args.receipments, merge=args.merge_messages),
            desc="encrypting",
        ):
            encrypted.append(m)
        encrypted = "\n---\n".join(encrypted)
        pyperclip.copy(encrypted)
        print(encrypted)

    if args.top_command in keys_cmd.aliases:
        keys = list(tqdm(keys_cmd(args), desc="keys"))
        print(tabulate(keys))
