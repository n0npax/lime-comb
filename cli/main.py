#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser(
    description="lime comb tool.")
parser.add_argument(
    "-t",
    "--to",
    dest="receipment",
    required=True,
    action="append",
    help="receipment of the message",
)
parser.add_argument(
    "-m", "--message", dest="message", required=False, action="append", help="message"
)
parser.add_argument(
    "-f", "--file", dest="file", required=False, action="append", help="file"
)
parser.add_argument(
    "--version",
    dest="version",
    required=False,
    action="store_true",
    help="show current version",
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="version",
    required=False,
    action="store_true",
    help="show current version",
)

args = parser.parse_args()
print(args.receipment)
