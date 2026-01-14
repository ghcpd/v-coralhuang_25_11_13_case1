"""
Flask application factory and initialization.
"""

from flask import Flask, g
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from config import DevConfig
from app.models import db, User
from app.email import mail
from app.locale import get_locale
from app.routes import register_basic_routes
from app.cli import register_cli


migrate = Migrate()
login_manager = LoginManager()
babel = Babel(locale_selector=lambda: None)  # Will be set during app creation

login_manager.login_view = "login"
login_manager.login_message = _l("Please log in to access this page.")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


def create_app(config_class=None):
    """
    Application factory function.
    
    Creates and configures a Flask application instance with all
    extensions and routes.
    
    Args:
        config_class: Configuration class to use. Defaults to DevConfig.
                     Should be TestConfig for tests.
    
    Returns:
        Flask application instance
    """
    if config_class is None:
        config_class = DevConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Initialize Babel with locale selector
    babel.init_app(app, locale_selector=get_locale)

    # Register blueprints and routes
    register_basic_routes(app)
    register_cli(app)

    # Set locale in g before each request
    @app.before_request
    def _set_locale_to_g():
        g.locale = get_locale()

    return app
