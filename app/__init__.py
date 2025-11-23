from flask import Flask
from .extensions import db, migrate, ma, jwt
from .errors import register_error_handlers
from config import Config
import os

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    # error handlers
    register_error_handlers(app)

    # routers
    from .routers import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
