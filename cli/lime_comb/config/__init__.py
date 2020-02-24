import os
from dataclasses import dataclass
from pathlib import Path

import yaml
from appdirs import user_config_dir, user_data_dir

from _collections import defaultdict
from password_generator import PasswordGenerator


@dataclass()
class Config:
    app_name = "lime-comb"

    data_dir = Path(user_data_dir(app_name))
    config_dir = Path(user_config_dir(app_name))

    config_file = config_dir / "config.yml"
    credentials_file = data_dir / "credentials"
    keyring_dir = data_dir / "keyring"
    oauth_gcp_conf = config_dir / "client-lime-comb.json"

    config_dir.mkdir(exist_ok=True, parents=True)
    data_dir.mkdir(exist_ok=True, parents=True)
    keyring_dir.mkdir(exist_ok=True, parents=True, mode=0o700)

    comment = "lime comb"

    @property
    def username(self):
        return self.__read_property("username")

    @username.setter
    def username(self, username):
        self.__save_property("username", username)

    @property
    def email(self):
        return self.__read_property("email")

    @email.setter
    def email(self, email):
        self.__save_property("email", email)

    @property
    def password(self):
        return self.__read_property("password")

    @password.setter
    def password(self, password):
        self.__save_property("password", password)

    @property
    def always_import(self):
        return self.__read_property("always_import", True)

    @always_import.setter
    def always_import(self, always_import):
        self.__save_property("always_import", bool(always_import))

    def __read_config(self):
        with open(self.config_file, "r") as f:
            _config = yaml.safe_load(f.read())
            if _config:
                return _config
        return {}

    def __write_config(self, conf):
        with open(self.config_file, "w") as f:
            f.write(yaml.dump(dict(conf)))

    def __read_property(self, name, default=None):
        conf = self.__read_config()
        if not conf:
            self._gen_config()
        return conf.get(name, default)

    def __save_property(self, name, value, validator=None):
        if validator:
            pass  # TODO
        conf = self.__read_config()
        conf[name] = value
        self.__write_config(conf)

    def _gen_config(self):
        print("Empty config detected. Setting up a new one")
        pwo = PasswordGenerator()
        pwo.minlen, pwo.maxlen = 30, 32
        password = pwo.generate()
        self.password = password
        self.username = input("username: ")
        self.email = input("email: ")


config = Config()
