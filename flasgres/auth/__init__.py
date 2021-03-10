from functools import wraps
import jwt
from flask import request, current_app as app, g
from flasgres.usuario import service as usuario_service
from flasgres.util.exception import AuthException
from .controller import auth_bp

def auth_required(_f):
    @wraps(_f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('session')
        if not token:
            raise AuthException(payload={ 'info': 'Sessão não encontrada' })
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario = usuario_service.get_usuario_by_login(data['username'])
        except Exception as exp:
            print(exp)
            raise AuthException(payload={ 'info': 'Sessão expirada ou é inválida' }) from exp
        setattr(g, 'usuario', usuario)
        return _f(*args, **kwargs)
    return decorated
