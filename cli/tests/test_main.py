import pytest
import sys
from main import parse_common, base_parser


@pytest.fixture
def parsers():
    return base_parser()


def test_parse_common_version(capsys, mocker, parsers):
    mocker.patch.object(sys, "exit")
    parser, _ = parsers
    args = parser.parse_args(["--version"])
    parse_common(args)

    assert sys.exit.called
    captured = capsys.readouterr()

    assert captured.out.startswith("version")
