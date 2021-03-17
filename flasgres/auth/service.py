from datetime import datetime, timedelta
import jwt
from flask import current_app as app
from werkzeug.security import check_password_hash
from flasgres.usuario import service
from flasgres.util import exception

def authenticate(credentials):
    usuario = service.get_usuario_by_login(credentials['login'])
    if not usuario or not check_password_hash(usuario.senha, credentials['senha']):
        raise exception.AuthException()

    token = jwt.encode({
        'id': usuario.id,
        'username': usuario.nome,
        'exp': datetime.now() + timedelta(hours=12)
    }, app.config['SECRET_KEY'])

    return usuario, token
