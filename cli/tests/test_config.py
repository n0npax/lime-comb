import builtins
from collections import defaultdict

import yaml

from lime_comb.config import config, validate_bool, EmptyConfigError

from .conftest import *


class TestConfig:
    def test_oauth_gcp_conf(self, oauth_gcp_conf, mocked_resp):
        with open(config.oauth_gcp_conf) as f:
            client_lime_comb_mocker_resp = f.read()
        assert client_lime_comb_mocker_resp == mocked_resp

    def test_get_config(self, mocker, email):
        mocker.patch.object(builtins, "input", return_value=email)
        mocker.patch.object(lime_comb.config, "validate_bool", return_value=True)
        mocker.patch.object(lime_comb.config, "validate_email", return_value=True)
        mocker.patch.object(lime_comb.config, "convert_bool_string", return_value=True)
        assert config.email == email

    def test_get_empty_config(self, mocker, email):
        mocker.patch.object(lime_comb.config.config, "_read_config", return_value={})
        with pytest.raises(EmptyConfigError):
            config._read_property("not_existing_property")
