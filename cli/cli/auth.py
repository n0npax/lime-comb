__author__ = "marcin.niemira@gmail.com (n0npax)"

import google
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/cloud-platform openid"


def get_cred(conf: str) -> google.oauth2.credentials.Credentials:
    flow = InstalledAppFlow.from_client_secrets_file(conf, scopes=scopes)

    cred = flow.run_local_server(
        host="localhost",
        port=5000,
        authorization_prompt_message="Please visit this URL: {url}",
        success_message="The auth flow is complete; you may close this window.",
        open_browser=True,
    )
    return cred
