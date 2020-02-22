import sys

import pytest

from main import base_parser, parse_common, EncryptCommand, enc_exec, dec_exec


def test_parse_common_version(capsys, mocker):
    mocker.patch.object(sys, "exit")
    base_parser(["--version"])
    assert sys.exit.called
    captured = capsys.readouterr()
    assert captured.out.startswith("version")


from cli.config import Config


def test_enc_cmd_plain_test_msg(capsys):
    args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-m", "test"])
    enc_exec(args, e_cmd)
    captured = capsys.readouterr()
    assert captured.out.startswith("-----BEGIN PGP MESSAGE---")


import tempfile


def test_enc_cmd_file_msg(capsys):
    with tempfile.NamedTemporaryFile() as fp:
        args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-f", fp.name])
        enc_exec(args, e_cmd)
        captured = capsys.readouterr()
        assert captured.out.startswith("-----BEGIN PGP MESSAGE---")
