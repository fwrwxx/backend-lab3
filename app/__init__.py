from flask import Flask
from .extensions import db, migrate, ma
from .errors import register_error_handlers
from config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # register error handlers
    register_error_handlers(app)

    # import and register blueprints here to avoid import-time errors
    from .routers import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app