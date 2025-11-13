"""
Routes for the application.
"""

from flask import render_template_string, g, request
from flask_login import login_required, login_user
from app.models import db, User


def register_basic_routes(app):
    """Register basic HTTP routes."""

    @app.route("/")
    def index():
        """Home page displaying current locale."""
        return render_template_string(
            "<p>current locale: {{ locale }}</p>", locale=g.get("locale", "unknown")
        )

    @app.route("/protected")
    @login_required
    def protected():
        """Protected page that requires authentication."""
        return "protected content"

    @app.route("/login")
    def login():
        """Login page that auto-creates a test user."""
        user = User.query.first()
        if not user:
            user = User(username="test", email="test@example.com", locale="zh")
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return "logged in"
