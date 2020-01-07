from appdirs import user_config_dir, user_data_dir
from pathlib import Path
import os
import yaml

OAUTH_GCP_CONF = "/home/n0npax/workspace/lime-comb/cli/client-lime-comb.json"


app_name = "lime-comb"

config_dir = Path(user_config_dir(app_name))
config_file = config_dir/"config.yml"
data_dir = Path(user_data_dir(app_name))
credentials_file = data_dir/"credentials"
keyring_dir = data_dir/"keyring"

config_dir.mkdir(exist_ok=True)
data_dir.mkdir(exist_ok=True)
keyring_dir.mkdir(exist_ok=True)

try:
    with open(config_file,'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error config file dont exist")