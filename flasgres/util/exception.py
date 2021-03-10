from werkzeug.exceptions import Unauthorized

class AuthException(Unauthorized):
    status_code = 401
    def __init__(self, payload=None):
        Unauthorized.__init__(self, 'Email ou Senha Inválidos')
        self.payload = payload

    def to_dict(self):
        _rv = dict(self.payload or ())
        _rv['description'] = self.description
        return _rv
