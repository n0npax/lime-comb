from uuid import uuid4

import pytest

from cli.auth.google import get_anon_cred
from cli.config import Config


@pytest.yield_fixture
def cred():
    with get_anon_cred() as c:
        yield c


@pytest.fixture
def domain():
    return "example.com"


@pytest.fixture
def email():
    return "jan.twardowski@example.com"


@pytest.fixture
def key_id():
    return uuid4()


@pytest.fixture
def priv_key():
    return "priv key data"


@pytest.fixture
def pub_key():
    return "pub key data"
