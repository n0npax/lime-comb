from cli.auth.google import get_anon_cred
from cli.config import Config
import pytest


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c
