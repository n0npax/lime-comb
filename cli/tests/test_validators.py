import builtins
from collections import defaultdict
from unittest.mock import MagicMock, patch

import yaml

import lime_comb
from lime_comb.validators.bool import validate_bool
from lime_comb.validators.email import lc_validate_email
from lime_comb.validators.file import validate_filepath

from .conftest import *


class TestValidator:
    @pytest.mark.parametrize(
        "file_path,raises", [("/etc/hosts", False), ("/no/such/file", True),],
    )
    def test_validate_filepath(self, file_path, raises):
        if raises:
            with pytest.raises(Exception):
                validate_filepath(file_path)
        else:
            assert validate_filepath(file_path)

    @pytest.mark.parametrize(
        "value,raises",
        [
            ("False", False),
            ("True", False),
            ("true", False),
            ("True", False),
            (True, False),
            (False, False),
            ("Some Value", True),
        ],
    )
    def test_validate_bool(self, value, raises):
        if raises:
            with pytest.raises(Exception):
                validate_bool(value)
        else:
            assert None == validate_bool(value)

    @pytest.mark.parametrize(
        "email,raises",
        [("llama", True), ("llama@llama", True), ("llama@llama.net", False),],
    )
    def test_lc_validate_email(self, email, raises):
        if raises:
            with pytest.raises(Exception):
                lc_validate_email(email)
        else:
            lc_validate_email(email)
