import os
from pathlib import Path

import yaml
from appdirs import user_config_dir, user_data_dir


class Config:
    app_name = "lime-comb"
    oauth_gcp_conf = "/home/n0npax/workspace/lime-comb/lime_comb/client-lime-comb.json"

    data_dir = Path(user_data_dir(app_name))
    config_dir = Path(user_config_dir(app_name))

    config_file = config_dir / "config.yml"
    credentials_file = data_dir / "credentials"
    keyring_dir = data_dir / "keyring"

    config_dir.mkdir(exist_ok=True, parents=True)
    data_dir.mkdir(exist_ok=True, parents=True)
    keyring_dir.mkdir(exist_ok=True, parents=True, mode=0o700)

    username: str = "marcin.niemira"
    email: str = "marcin.niemira@gmail.com"
    comment: str = "Lime Comb"

    password: str = "dupa.8Polska12"

    always_import: bool = False


try:
    with open(Config.config_file, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error config file dont exist")
