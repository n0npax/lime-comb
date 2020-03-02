import pytest
from semver import parse

from lime_comb import __version__


@pytest.mark.parametrize(
    "version_adj", ["major", "minor", "patch"],
)
def test_version(version_adj):
    version = parse(__version__)
    assert version
    assert isinstance(version[version_adj], int)
