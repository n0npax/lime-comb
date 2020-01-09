import pytest

from cli.auth.google import get_anon_cred
from cli.config import Config


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c
