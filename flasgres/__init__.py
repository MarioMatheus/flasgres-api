import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import DeclarativeMeta
from .util.serialize import AlchemyEncoder

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

def create_app(test_config=None):
    app = FlasgresFlask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .controller import root_bp
    app.register_blueprint(root_bp)

    from .usuario import usuario_bp
    app.register_blueprint(usuario_bp)

    return app
