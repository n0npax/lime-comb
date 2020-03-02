__author__ = "marcin.niemira@gmail.com (n0npax)"

import pickle  # nosec
from contextlib import contextmanager

import google
from google_auth_oauthlib.flow import InstalledAppFlow

from lime_comb.config import config
from lime_comb.logger.logger import logger

__scopes = " ".join(
    [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/cloud-platform",
        "openid",
    ]
)


def web_login(conf: str):
    flow = InstalledAppFlow.from_client_secrets_file(conf, scopes=__scopes)
    return flow.run_local_server(
        host="localhost",
        port=5000,
        authorization_prompt_message="Please visit this URL: {url}",
        success_message="The auth flow is complete; you may close this window.",
        open_browser=True,
    )


@contextmanager
def get_cred(conf: str) -> google.oauth2.credentials.Credentials:
    try:
        cred = read_creds()
    except Exception as e:
        logger.warning(e)
        cred = None
    if cred and not cred.expired:
        yield cred
    else:
        logger.warning(f"Error, fallback to fresh login")
        cred = web_login(conf)
        save_creds(cred)
        yield cred


@contextmanager
def get_anon_cred() -> google.auth.credentials.Credentials:
    yield google.auth.credentials.AnonymousCredentials()


def save_creds(cred):
    pickle.dump(cred, open(config.credentials_file, "wb"))


def read_creds():
    return pickle.load(open(config.credentials_file, "rb"))  # nosec
