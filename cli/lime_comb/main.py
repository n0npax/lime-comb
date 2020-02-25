#!/usr/bin/env python3
import argparse
import sys

import pyperclip
from tabulate import tabulate
from tqdm import tqdm

import lime_comb
from lime_comb.commands.decrypt import DecryptCommand
from lime_comb.commands.encrypt import EncryptCommand
from lime_comb.commands.keys import KeysCommand
from lime_comb.logger.logger import logger


def base_parser(input_args):
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
        required=False,
        dest="top_command",
    )
    keys_cmd = KeysCommand(subparsers)
    enc_cmd = EncryptCommand(subparsers)
    dec_cmd = DecryptCommand(subparsers)
    args = parser.parse_args(input_args)
    parse_common(parser, args)
    return args, keys_cmd, enc_cmd, dec_cmd, None


# TODO provide class for config and keys


def parse_common(parser, args):
    logger.setLevel(args.log_lvl)

    logger.info(f"log lvl {logger.getEffectiveLevel()}")
    if args.version:
        print(f"version: {lime_comb.__version__}")
        sys.exit(0)
    elif not args.top_command:
        parser.print_help()
        sys.exit(0)


def get_recipients(args):
    if not getattr(args, "recipients", None):
        logger.info("No recipients. Asking user to type in")
        args.recipients = input("please specify recipients(space separated)\n").split()
    return args.recipients


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


def dec_exec(args, cmd):
    if args.top_command in cmd.aliases:
        decrypted = []
        for m in tqdm(cmd(get_message(args)), desc="decrypting"):
            decrypted.append(m)
        decrypted = "\n---\n".join(decrypted)
        pyperclip.copy(decrypted)
        return decrypted


def enc_exec(args, cmd):
    if args.top_command in cmd.aliases:
        encrypted = []
        for m in tqdm(
            cmd(get_message(args), get_recipients(args), merge=args.merge_messages),
            desc="encrypting",
        ):
            encrypted.append(m)
        encrypted = "\n---\n".join(encrypted)
        pyperclip.copy(encrypted)
        return encrypted


def keys_exec(args, cmd):
    if args.top_command in cmd.aliases:
        keys = list(tqdm(cmd(args), desc="keys"))
        return tabulate(keys)


def main(cmdline_args):
    args, k_cmd, e_cmd, d_cmd, _ = base_parser(cmdline_args)
    for action in (
        dec_exec(args, d_cmd),
        enc_exec(args, e_cmd),
        keys_exec(args, k_cmd),
    ):
        if action:
            print(action)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
