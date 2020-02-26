import builtins

from lime_comb.config import config

from .conftest import *


class TestConfig:
    def test_oauth_gcp_conf(self, oauth_gcp_conf, mocked_resp):
        client_lime_comb_file = config.oauth_gcp_conf
        with open(client_lime_comb_file) as f:
            client_lime_comb_mocker_resp = f.read()
        assert client_lime_comb_mocker_resp == mocked_resp

    def test_get_config(self, mocker):
        test_email = "llama@llama.net"
        mocker.patch.object(builtins, "input", return_value=test_email)
        config._gen_config()
        assert config.email == test_email
