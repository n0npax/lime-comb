from functools import wraps

import google.oauth2.id_token
from flask import current_app, g, request
from google.auth.transport import requests
from werkzeug.exceptions import Unauthorized

google_requests = requests.Request()


def jwt_validate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = request.cookies.get("token", None) or request.headers.get(
            "X-API-KEY", None
        )

        if not id_token:
            raise Unauthorized("Token is missing")
        try:
            claims = google.oauth2.id_token.verify_oauth2_token(
                id_token, google_requests,  # TODO add audience
            )
            g.email = claims["email"]
        except Exception as e:
            current_app.logger.info(f"login failed: {e}")
            raise Unauthorized(f"Auth failed {e}")
        return f(*args, **kwargs)

    return decorated_function
