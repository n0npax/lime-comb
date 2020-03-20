import pytest

from lime_comb_api.auth import jwt_validate


def test_auth():
    @jwt_validate
    def f(*args, **kwargs):
        pass

    with pytest.raises(Exception):
        f()
