from functools import wraps
import traceback
import json
import jwt
from jose import jwt as jose_jwt
from flask import request, current_app as app, g
from six.moves.urllib.request import urlopen
from flasgres.usuario import service as usuario_service
from flasgres.util.exception import AuthException
from .controller import auth_bp

def auth(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['id']
    except Exception as exp:
        traceback.print_exc()
        raise AuthException(payload={
            'info': 'Sessão expirada ou é inválida'
        }) from exp

def oauth(token):
    jsonurl = urlopen("https://" + app.config['AUTH0_DOMAIN'] + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
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
            payload = jose_jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=app.config['AUTH0_AUDIENCE'],
                issuer='https://' + app.config['AUTH0_DOMAIN'] + '/'
            )
        except Exception as exp:
            traceback.print_exc()
            raise AuthException(payload={ 'info': 'Sessão expirada ou é inválida' }) from exp

    return payload['email']

def auth_required(_f):
    @wraps(_f)
    def decorated(*args, **kwargs):
        if request.headers.get('auth_test') or not app.testing:
            token = request.cookies.get('session')
            if not token:
                raise AuthException(payload={ 'info': 'Sessão não encontrada' })
            if token.startswith("oauth"):
                login = oauth(token.split()[1])
                usuario = usuario_service.get_usuario_by_login(login)
            else:
                usuario_id = auth(token)
                usuario = usuario_service.get_usuario(usuario_id)
            if usuario is None:
                raise AuthException(payload={ 'info': 'Sessão expirada ou é inválida' })
            setattr(g, 'usuario', usuario)
        return _f(*args, **kwargs)
    return decorated
