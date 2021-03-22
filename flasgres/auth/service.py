from datetime import datetime, timedelta
import jwt
from flask import current_app as app
from werkzeug.security import check_password_hash
from flasgres.usuario import service as usuario_service
from flasgres.util import exception

def authenticate(credentials):
    usuario = usuario_service.get_usuario_by_login(credentials['login'])
    try:
        checked_password = check_password_hash(usuario.senha, credentials['senha'])
    except Exception as exp:
        raise exception.AuthException({ 'op': str(exp) }) from exp
    if not usuario or not checked_password:
        raise exception.AuthException()

    return usuario, get_token_from(usuario)

def get_token_from(usuario):
    return jwt.encode({
        'id': usuario.id,
        'username': usuario.nome,
        'exp': datetime.now() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])

def get_cookie_options():
    return dict(
        max_age=timedelta(hours=24),
        samesite='None' if app.config['APP_ENV'] == 'production' else None,
        secure=True if app.config['APP_ENV'] == 'production' else None,
    )
