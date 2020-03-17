import builtins
from collections import defaultdict
from unittest.mock import MagicMock, patch

import yaml

import lime_comb
from lime_comb.config import EmptyConfigError, config

from .conftest import *


class TestConfig:
    def test_oauth_gcp_conf(self, oauth_gcp_conf, mocked_resp):
        with open(config.oauth_gcp_conf) as f:
            client_lime_comb_mocker_resp = f.read()
        assert client_lime_comb_mocker_resp == mocked_resp

    def test_get_config(self, mocker, uuid, existing_config):
        new_username = uuid
        mocker.patch.object(builtins, "input", return_value=new_username)
        mocker.patch.object(lime_comb.config, "convert_bool_string", return_value=True)

        with patch("lime_comb.config.validate_bool") as validate_bool_mock:
            with patch("lime_comb.config.lc_validate_email") as validate_email_mock:
                validate_bool_mock.return_value = True
                validate_email_mock.return_value = True
                config._gen_config()
                assert config.username == new_username

    def test_read_not_existing_property(self, mocker, email):
        mocker.patch.object(lime_comb.config.config, "_read_config", return_value={})
        with pytest.raises(EmptyConfigError):
            config._read_property("not_existing_property")

    @pytest.mark.noautofixt
    def test_read_not_existing_config(self):
        assert {} == config._read_config()

    def test_rptr(self):
        assert "Config" in str(config)

    def test_save_username(self, uuid):
        config.username = uuid
        assert config.username == uuid

    def test_save_password(self, uuid):
        config.password = uuid
        assert config.password == uuid

    @pytest.mark.parametrize(
        "input_email,raises",
        [("llama@llama.net", False), ("llama", True), ("llama@llama", True),],
    )
    @pytest.mark.noautofixt
    def test_save_email(self, input_email, raises):
        if raises:
            with pytest.raises(Exception):
                config.email = input_email
        else:
            config.email = input_email
            assert config.email == input_email

    @pytest.mark.parametrize(
        "export_password,raises,value",
        [
            ("llama", True, None),
            ("False", False, False),
            ("false", False, False),
            ("True", False, True),
            ("true", False, True),
            ("llama", True, None),
            (True, False, True),
            (False, False, False),
        ],
    )
    def test_export_password(self, export_password, raises, value):
        if raises:
            with pytest.raises(Exception):
                config.export_password = export_password
        else:
            config.export_password = export_password
            assert config.export_password == value

    @pytest.mark.parametrize(
        "input_value,expected_value,default",
        [
            ("False", False, None),
            ("false", False, None),
            ("True", True, None),
            ("", True, True),
            ("", False, False),
        ],
    )
    def test_get_bool(self, mocker, input_value, expected_value, default):
        mocker.patch.object(builtins, "input", return_value=input_value)
        actual_value = config.get_bool("", default=default)
        assert actual_value == expected_value
