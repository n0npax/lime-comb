import os

from functools import wraps

import google.oauth2.id_token
from flask import request, g, current_app
from google.auth.transport import requests
from werkzeug.exceptions import Unauthorized

firebase_request_adapter = requests.Request()


def jwt_validate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = request.cookies.get("token", None) or request.headers.get(
            "X-API-KEY", None
        )
        if not id_token:
            raise Unauthorized("Token is missing")
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token,
                firebase_request_adapter
                # , 'wiatrolap.web.app'
            )
            g.user_id = claims["user_id"]
        except Exception as e:
            current_app.logger.info(f"login failed: {e}")
            raise Unauthorized("Auth failed")
        return f(*args, **kwargs)

    return decorated_function
