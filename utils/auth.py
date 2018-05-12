from os import environ as env
from functools import wraps
import json

import requests
import redis
from flask import request, _request_ctx_stack
from flask_restful import abort
from jose import jwt

AUTH0_DOMAIN = 'recommend-app.eu.auth0.com'
API_AUDIENCE = 'https://recommend-api.herokuapp.com'
ALGORITHMS = ['RS256']
JWKS_EXPIRE = 3600


cache = redis.from_url(env['REDIS_URL'])


def _get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        abort(401, code="authorization_header_missing", description="Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        abort(401, code="invalid_header", description="Authorization header must start with Bearer")
    elif len(parts) == 1:
        abort(401, code="invalid_header", description="Token not found")
    elif len(parts) > 2:
        abort(401, code="invalid_header", description="Authorization header must be Bearer token")

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token_auth_header()

        jwks_raw = cache.get('auth0_jwks')
        if not jwks_raw:
            jwks = requests.get('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).json()
            cache.set('auth0_jwks', json.dumps(jwks), JWKS_EXPIRE)
        else:
            jwks = json.loads(jwks_raw)

        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://{}/'.format(AUTH0_DOMAIN)
                )
            except jwt.ExpiredSignatureError:
                abort(401, code="token_expired", description="token is expired")
            except jwt.JWTClaimsError:
                abort(401, code="decode_error", description="decoding token threw errors")
            except Exception:
                abort(401, code="invalid_header", description="Unable to parse auth token")

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)

        abort(401, code="invalid_header", description="Unable to find appropriate key")

    return decorated
