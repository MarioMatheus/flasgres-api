import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import DeclarativeMeta
from .util.serialize import AlchemyEncoder
from .util.exception import AuthException

db = SQLAlchemy()
migrate = Migrate()

class FlasgresFlask(Flask):
    json_encoder = AlchemyEncoder

    def make_response(self, rv):
        if isinstance(rv.__class__, DeclarativeMeta) or isinstance(rv, list):
            new_rv = jsonify(rv)
        elif isinstance(rv, tuple) and isinstance(rv[1], int):
            new_rv = jsonify(rv[0]), rv[1]
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
    app = FlasgresFlask(__name__)
    app.config.from_object(config or os.environ['APP_SETTINGS'])

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_default_exceptions(AuthException)

    from .controller import root_bp
    app.register_blueprint(root_bp)

    from .usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
