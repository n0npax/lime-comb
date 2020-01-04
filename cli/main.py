#!/usr/bin/env python3
import argparse
import sys
import logging

import cli

parser = argparse.ArgumentParser(
    description="lime comb tool.")
parser.add_argument(
    "-t",
    "--to",
    dest="receipments",
    required=False,
    action="append",
    help="receipment of the message",
)
parser.add_argument(
    "-m", "--message", dest="messages", required=False, action="append", help="message", default=[]
)
parser.add_argument(
    "-f", "--file", dest="files", required=False, action="append", help="file", default=[]
)
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
    default="DEBUG",
    action="store",
    choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
    help="log level",
)

args = parser.parse_args()
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(name=cli.__app_name__)
    
def main():
    logger.setLevel(args.log_lvl)
    logger.debug(f"log lvl {logger.getEffectiveLevel()}")
    if args.version:
        print(f"version: {cli.__version__}")
        sys.exit(0)
    if not args.receipments:
        logger.debug("No receipmens. Asking userto type in")
        args.receipments = input("please specify receipments(space separated)\n")
    if args.files:
        for fn in args.files:
            with open(fn, 'r') as f:
                args.messages.append(f.read())


if __name__ == "__main__":
    main()