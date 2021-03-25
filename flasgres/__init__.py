import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import DeclarativeMeta
from .util.serialize import AlchemyEncoder, AlchemyJSON
from .util.exception import AuthException, BusinessException

db = SQLAlchemy()
migrate = Migrate()

class FlasgresFlask(Flask):
    def make_response(self, rv):
        def is_sql_model(_e):
            return issubclass(_e.__class__, AlchemyJSON)

        if is_sql_model(rv):
            new_rv = rv.json()
        elif isinstance(rv, tuple) and is_sql_model(rv[0]) and isinstance(rv[1], int):
            new_rv = rv[0].json(), rv[1]
        elif isinstance(rv, list):
            _list = list(map(lambda e: e.json() if is_sql_model(e) else e, rv))
            new_rv = jsonify(_list)
        else:
            new_rv = rv

        return super().make_response(new_rv)

    def register_default_exceptions(self, *exceptions):
        def error_handler(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response
        return [self.register_error_handler(ex, error_handler) for ex in exceptions]

def create_app(config=None):
    app = FlasgresFlask(__name__, instance_relative_config=True)
    app.config.from_object(config or os.environ['APP_SETTINGS'])

    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_default_exceptions(AuthException, BusinessException)

    from .controller import root_bp
    app.register_blueprint(root_bp)

    from .usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
