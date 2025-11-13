from flask import g, render_template_string, get_flashed_messages
from flask_login import login_required

from .models import User, db


def register_routes(app):
    """Register the basic application routes."""

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
        user = User.query.first()
        if not user:
            user = User(username="test", email="test@example.com", locale="zh")
            db.session.add(user)
            db.session.commit()

        messages = get_flashed_messages()
        return render_template_string(
            "{% for message in messages %}<p>{{ message }}</p>{% endfor %}"
            "<p>current locale: {{ locale }}</p><p>login page</p>",
            messages=messages,
            locale=g.get("locale", "unknown"),
        )
