from flask import current_app, g, request, render_template_string
from flask_login import login_required, login_user, current_user
from flask_babel import lazy_gettext as _l

from .models import User
from . import login_manager


def register_basic_routes(app):
    # localized login message for tests and normal usage
    login_manager.login_message = _l("Please log in to access this page.")

    @app.route("/")
    def index():
        return render_template_string(
            "<p>current locale: {{ locale }}</p>", locale=g.get("locale", "unknown")
        )

    @app.route("/protected")
    @login_required
    def protected():
        return "protected content"

    from flask import flash, render_template_string

    @app.route("/login", methods=["GET"])    
    def login():
        # A real login page that displays flashed messages (used by login_required)
        from flask import get_flashed_messages

        messages = get_flashed_messages()
        return render_template_string("<p>login page: {{ messages }}</p>", messages=messages)

    @app.route("/login-auto")
    def login_auto():
        # Helper used in tests: create or reuse a test user and log them in
        user = User.query.first()
        if not user:
            user = User(username="test", email="test@example.com", locale="zh")
            from . import db

            db.session.add(user)
            db.session.commit()
        login_user(user)
        return "logged in"
