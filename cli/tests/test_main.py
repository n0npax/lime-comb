import builtins
import sys
import tempfile
from uuid import uuid4

import pyperclip
import pytest

from cli.config import Config
from main import *


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
        output = enc_exec(args, e_cmd)
        assert output.startswith("-----BEGIN PGP MESSAGE---")

    def test_enc_cmd_file_msg(self, mocker):
        mocker.patch.object(pyperclip, "copy")
        with tempfile.NamedTemporaryFile() as fp:
            args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-f", fp.name])
            output = enc_exec(args, e_cmd)
            assert output.startswith("-----BEGIN PGP MESSAGE---")

    def test_dec_cmd(self, mocker):
        base_test_message = str(uuid4())
        mocker.patch.object(pyperclip, "copy")
        args, _, e_cmd, _, _ = base_parser(
            ["e", "-t", Config.email, "-m", base_test_message]
        )
        enc_msg = enc_exec(args, e_cmd)
        args, _, _, d_cmd, _ = base_parser(["d", "-m", enc_msg])
        dec_msg = dec_exec(args, d_cmd)
        assert dec_msg == base_test_message


def test_main(mocker, capsys):
    mocker.patch.object(sys, "exit")
    main(["--help"])
    assert sys.exit.called
    captured = capsys.readouterr()
    assert "--help" in captured.out
