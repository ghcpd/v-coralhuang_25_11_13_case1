import threading

from flask import Flask, g, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel


# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()

# Match our routes — we keep login view as 'login' to match register_basic_routes
login_manager.login_view = "login"


def create_app(config_class=None):
    """Application factory."""
    app = Flask(__name__)

    if config_class is None:
        # Default to a base configuration that includes i18n defaults
        from .config import DevConfig

        config_class = DevConfig

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    # Register plumbing
    from .routes import register_basic_routes
    from .cli import register_cli

    register_basic_routes(app)
    register_cli(app)

    # easy way to put locale on g
    @app.before_request
    def _set_locale_to_g():
        from . import locale

        # call get_locale from our package-level module
        g.locale = locale.get_locale()

    return app
