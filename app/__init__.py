from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from .translations import get_locale


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()


login_manager.login_view = "login"
login_manager.login_message = _l("Please log in to access this page.")


def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        # sensible default
        from config import DevConfig

        app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    # pass our selector function explicitly
    babel.init_app(app, locale_selector=get_locale)

    # import blueprints and regs
    from .routes import register_basic_routes
    from .cli import register_cli

    register_basic_routes(app)
    register_cli(app)

    return app
