import builtins
import sys
import tempfile

import pytest

from cli.config import Config
from main import (EncryptCommand, base_parser, dec_exec, enc_exec,
                  get_receipments, parse_common)


def test_parse_common_version(capsys, mocker):
    mocker.patch.object(sys, "exit")
    base_parser(["--version"])
    assert sys.exit.called
    captured = capsys.readouterr()
    assert captured.out.startswith("version")




def test_enc_cmd_plain_test_msg(capsys):
    args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-m", "test"])
    enc_exec(args, e_cmd)
    captured = capsys.readouterr()
    assert captured.out.startswith("-----BEGIN PGP MESSAGE---")




def test_enc_cmd_file_msg(capsys):
    with tempfile.NamedTemporaryFile() as fp:
        args, _, e_cmd, _, _ = base_parser(["e", "-t", Config.email, "-f", fp.name])
        enc_exec(args, e_cmd)
        captured = capsys.readouterr()
        assert captured.out.startswith("-----BEGIN PGP MESSAGE---")




def test_get_receipments(mocker):
    mocker.patch.object(builtins, "input", return_value="test_input")
    args, _, _, _, _ = base_parser(["e"])
    receipments = get_receipments(args)
    assert receipments == ["test_input"]
