from flask import render_template_string, g, request, current_app, flash, get_flashed_messages
from flask_login import login_required, login_user
from .models import User
from . import db, login_manager, babel
from .translations import get_locale


def register_basic_routes(app):

    @app.before_request
    def _set_locale_to_g():
        g.locale = get_locale()


    @app.route("/")
    def index():
        return render_template_string(
            "<p>current locale: {{ locale }}</p>", locale=g.get("locale", "unknown")
        )

    @app.route("/protected")
    @login_required
    def protected():
        return "protected content"

    @app.route("/login")
    def login():
        # Create or retrieve a user and log them in
        user = User.query.first()
        if not user:
            user = User(username="test", email="test@example.com", locale="zh")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        # Render a page showing flashed messages (e.g., login_required message)
        raw_messages = get_flashed_messages()
        # apply simple translation mapping provided via config if available
        translations = current_app.config.get("TRANSLATIONS", {})
        locale = g.get("locale", current_app.config.get("BABEL_DEFAULT_LOCALE"))
        mapped = []
        for m in raw_messages:
            mapped.append(translations.get(locale, {}).get(m, m))
        return render_template_string(
            "<p>{{ messages|join('\n') }}</p><p>logged in</p>", messages=mapped
        )
