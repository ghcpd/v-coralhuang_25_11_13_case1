import os

from flask import Flask, current_app, g, request
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l

from config import DevConfig, TestConfig
from .models import db, User
from .email import mail
from .routes import register_routes
from .cli import register_cli

login_manager = LoginManager()
migrate = Migrate()
babel = Babel()

login_manager.login_view = "login"
login_manager.login_message = _l("Please log in to access this page.")

CONFIGURATION_MAP = {
    "dev": DevConfig,
    "development": DevConfig,
    "test": TestConfig,
}


def create_app(configuration=None):
    """Create an application configured for the desired environment."""

    if configuration is None:
        configuration = os.environ.get("FLASK_CONFIG", "dev")

    if isinstance(configuration, str):
        config_class = CONFIGURATION_MAP.get(configuration, DevConfig)
    else:
        config_class = configuration

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    register_routes(app)
    register_cli(app)

    @app.before_request
    def set_locale_to_g():
        g.locale = get_locale()

    return app


def get_locale():
    """Determine the best match between user locale and allowed languages."""

    if current_user.is_authenticated and current_user.locale:
        return current_user.locale

    languages = current_app.config["LANGUAGES"]
    return request.accept_languages.best_match(languages)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
