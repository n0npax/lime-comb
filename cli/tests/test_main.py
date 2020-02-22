import builtins
import sys
import tempfile

import pyperclip
import pytest

from cli.config import Config
from main import (EncryptCommand, base_parser, dec_exec, enc_exec,
                  get_receipments, parse_common)


class TestHelperFunctions:
    def test_parse_common_version(self, capsys, mocker):
        mocker.patch.object(sys, "exit")
        base_parser(["--version"])
        assert sys.exit.called
        captured = capsys.readouterr()
        assert captured.out.startswith("version")

    def test_get_receipments(self, mocker):
        mocker.patch.object(builtins, "input", return_value="test_input")
        args, _, _, _, _ = base_parser(["e"])
        receipments = get_receipments(args)
        assert receipments == ["test_input"]


class TestCommandObjects:
    def test_enc_cmd_plain_test_msg(self, mocker, capsys):
        mocker.patch.object(pyperclip, "copy")
        args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-m", "test"])
        enc_exec(args, e_cmd)
        captured = capsys.readouterr()
        assert captured.out.startswith("-----BEGIN PGP MESSAGE---")

    def test_enc_cmd_file_msg(self, mocker, capsys):
        mocker.patch.object(pyperclip, "copy")
        with tempfile.NamedTemporaryFile() as fp:
            args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-f", fp.name])
            enc_exec(args, e_cmd)
            captured = capsys.readouterr()
            assert captured.out.startswith("-----BEGIN PGP MESSAGE---")
