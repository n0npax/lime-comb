import secrets
import string
from dataclasses import dataclass
from pathlib import Path

import requests
import yaml
from appdirs import user_config_dir, user_data_dir
from email_validator import EmailSyntaxError

from lime_comb.logger.logger import logger
from lime_comb.validators.bool import validate_bool
from lime_comb.validators.email import lc_validate_email


@dataclass()
class Config:
    app_name = "lime-comb"

    data_dir = Path(user_data_dir(app_name))
    config_dir = Path(user_config_dir(app_name))

    client_lime_comb_url = "http://lime-comb.web.app/_client-lime-comb.json"
    config_file = config_dir / "config.yml"
    oauth_client_config = config_dir / "client-lime-comb.json"
    credentials_file = data_dir / "credentials"
    keyring_dir = data_dir / "keyring"

    config_dir.mkdir(exist_ok=True, parents=True)
    data_dir.mkdir(exist_ok=True, parents=True)
    keyring_dir.mkdir(exist_ok=True, parents=True, mode=0o700)

    comment = "lime comb"
    __raised = False

    @property
    def oauth_gcp_conf(self):
        path = self.oauth_client_config
        if not path.exists():
            try:
                logger.info(f"fetching {self.client_lime_comb_url}")
                response = requests.get(self.client_lime_comb_url)
                response.raise_for_status()
                with open(str(path), "w") as f:
                    f.write(response.content.decode("utf-8"))
            except Exception as e:
                logger.error(f"Error {e} during fetching client-lime-comb.json")
        return path

    def get_configurable(self):
        return {
            "username": self.username,
            "email": self.email,
            "always_import": self.always_import,
            "password": self.password,
            "export_priv_key": self.export_priv_key,
            "export_password": self.export_password,
        }

    def __repr__(self):
        return f"Config: ({self.get_configurable()}) & constant values"

    @property
    def username(self):
        return self._read_property("username")

    @username.setter
    def username(self, username):
        self.__save_property("username", username)

    @property
    def password(self):
        return self._read_property("password")

    @password.setter
    def password(self, password):
        self.__save_property("password", password)

    @property
    def email(self):
        return self._read_property("email")

    @email.setter
    def email(self, email):
        self.__save_property("email", email, lc_validate_email)

    @property
    def export_password(self):
        return self._read_property("export_password", True)

    @export_password.setter
    def export_password(self, value):
        self.__save_property(
            "export_password", convert_bool_string(value), validate_bool
        )

    @property
    def export_priv_key(self):
        return self._read_property("export_priv_key", True)

    @export_priv_key.setter
    def export_priv_key(self, value):
        self.__save_property(
            "export_priv_key", convert_bool_string(value), validate_bool
        )

    @property
    def always_import(self):
        return self._read_property("always_import", True)

    @always_import.setter
    def always_import(self, value):
        self.__save_property("always_import", convert_bool_string(value), validate_bool)

    def _read_config(self):
        try:
            with open(self.config_file, "r") as f:
                _config = yaml.safe_load(f.read())
                if _config:
                    return _config
            return {}
        except FileNotFoundError:
            self.config_file.touch(mode=0o600)
            return {}

    def __write_config(self, conf):
        with open(self.config_file, "w") as f:
            f.write(yaml.dump(dict(conf)))

    def _read_property(self, name, default=None):
        conf = self._read_config()
        if not conf and not self.__raised:
            logger.error(f"config is empty")
            self.__raised = True
            raise EmptyConfigError("Empty Config")
        if name in conf.keys():
            return conf[name]
        return default

    def __save_property(self, name, value, validator=None):
        if validator:
            validator(value)
        conf = self._read_config()
        conf[name] = value
        self.__write_config(conf)

    @classmethod
    def _config_input(cls, property_name, *, default=None):
        value = None
        while True:
            value = input(f"{property_name} (suggested {default}): ") or default
            if value:
                return value

    def _gen_config(self):
        print("-" * 44)
        print("Empty config detected. Setting up a new one")
        if not self.password:
            alphabet = string.ascii_letters + string.digits
            self.password = "".join(secrets.choice(alphabet) for i in range(32))
        self.password = self._config_input("password", default=self.password)
        self.username = self._config_input("username", default=self.username)
        while True:
            try:
                self._config_input("email", default=self.email)
                break
            except EmailSyntaxError as e:
                logger.error(e)
        self.export_password = self.get_bool(
            "export_password: (suggested true)", default=self.export_password
        )
        self.export_priv_key = self.get_bool(
            "export_priv_key (suggested true)", default=self.export_priv_key
        )
        self.always_import = self.get_bool(
            "always_import (suggested true)", default=self.always_import
        )
        print("-" * 44)

    @classmethod
    def get_bool(cls, message, *, default=None):
        while True:
            my_bool = input(f"{message} [True/False]: ")
            if my_bool == "" and default != None:
                return default
            try:
                validate_bool(my_bool)
                break
            except ValueError:
                logger.warning(f"{my_bool} is not True or False")
        return convert_bool_string(my_bool)


def convert_bool_string(my_bool):
    if isinstance(my_bool, bool):
        return my_bool
    if isinstance(my_bool, (str)):
        return {"true": True, "false": False}[my_bool.lower()]
    return False


class EmptyConfigError(Exception):
    pass


config = Config()
