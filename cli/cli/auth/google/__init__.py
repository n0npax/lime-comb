__author__ = "marcin.niemira@gmail.com (n0npax)"

import google
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from contextlib import contextmanager


scopes = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/cloud-platform openid"
# https://www.googleapis.com/auth/datastore

@contextmanager
def get_cred(conf: str) -> google.oauth2.credentials.Credentials:

    try:
        cred = read_creds()
        if cred.expired:
            request = google.auth.transport.requests.Request()
            cred.refresh(request)
            if cred.expired:
                #TODO WARN
                raise Exception("cannot refresh creds")
            yield cred
        yield cred

    except:
        flow = InstalledAppFlow.from_client_secrets_file(conf, scopes=scopes)

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
    pickle.dump(cred,open('/home/n0npax/.lime-comb/creds','wb'))

def read_creds():
    return pickle.load(open('/home/n0npax/.lime-comb/creds','rb'))