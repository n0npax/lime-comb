__author__ = "marcin.niemira@gmail.com (n0npax)"

import pickle
from contextlib import contextmanager

import google
from google_auth_oauthlib.flow import InstalledAppFlow

from cli.config import Config
from cli.logger.logger import logger

__scopes = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/cloud-platform openid"


@contextmanager
def get_cred(conf: str) -> google.oauth2.credentials.Credentials:

    try:
        cred = read_creds()
        if cred.expired:
            request = google.auth.transport.requests.Request()
            cred.refresh(request)
            if cred.expired:
                logger.warning(
                    "existing credentials are expired and cannot be refreshed"
                )
                raise Exception("cannot refresh creds")
            yield cred
        yield cred

    except Exception as err:
        logger.warning(f"Error: {err}, fallback to fresh login")
        flow = InstalledAppFlow.from_client_secrets_file(conf, scopes=__scopes)
        cred = flow.run_local_server(
            host="localhost",
            port=5000,
            authorization_prompt_message="Please visit this URL: {url}",
            success_message="The auth flow is complete; you may close this window.",
            open_browser=True,
        )
        save_creds(cred)
        yield cred


@contextmanager
def get_anon_cred() -> google.auth.credentials.Credentials:
    yield google.auth.credentials.AnonymousCredentials()


def save_creds(cred):
    pickle.dump(cred, open(Config.credentials_file, "wb"))


def read_creds():
    return pickle.load(open(Config.credentials_file, "rb"))
