from werkzeug.exceptions import Unauthorized, BadRequest

class AuthException(Unauthorized):
    status_code = 401
    def __init__(self, payload=None):
        Unauthorized.__init__(self, 'Email ou Senha Inválidos')
        self.payload = payload

    def to_dict(self):
        _rv = dict(self.payload or ())
        _rv['description'] = self.description
        return _rv

class BusinessException(BadRequest):
    status_code = 400
    def __init__(self, payload=None):
        BadRequest.__init__(self, 'Operação Inválida')
        self.payload = payload

    def to_dict(self):
        _rv = dict(self.payload or ())
        _rv['description'] = self.description
        return _rv
