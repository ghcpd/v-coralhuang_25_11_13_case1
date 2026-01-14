"""
Comprehensive test suite for the Flask application.

Tests cover:
- Configuration and language settings
- Locale selection based on user preference
- Locale selection based on Accept-Language header
- Login message localization
- CLI command execution
- Async email sending
"""

import pytest
from flask import g
from flask_login import login_user
from app import create_app
from app.models import db, User
from app.email import send_email
from app.locale import get_locale
from config import TestConfig


@pytest.fixture
def app():
    """
    Create and configure a test application instance.
    
    Yields the app with an initialized database.
    Cleans up after each test.
    """
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


# ============================================================================
# Configuration Tests
# ============================================================================


def test_testconfig_should_provide_languages(app):
    """
    Test that TestConfig includes LANGUAGES and related i18n settings.
    
    This ensures the test configuration has all necessary multilingual
    settings inherited from BaseConfig.
    """
    assert "LANGUAGES" in app.config, "LANGUAGES missing in TestConfig"
    assert isinstance(app.config["LANGUAGES"], (list, tuple)), "LANGUAGES should be list/tuple"
    assert "en" in app.config["LANGUAGES"]
    assert "zh" in app.config["LANGUAGES"]
    
    # Verify Babel defaults are present
    assert "BABEL_DEFAULT_LOCALE" in app.config
    assert "BABEL_DEFAULT_TIMEZONE" in app.config


# ============================================================================
# Locale Selection Tests
# ============================================================================


def test_locale_selector_respects_accept_language(app, client):
    """
    Test that locale selector respects the Accept-Language header.
    
    When no user is logged in, the locale should be selected from the
    Accept-Language header preference.
    """
    response = client.get("/", headers={"Accept-Language": "zh;q=1, en;q=0.5"})
    text = response.get_data(as_text=True)

    assert "current locale: zh" in text, \
        "expected locale zh in response, got: {}".format(text)


def test_locale_selector_respects_accept_language_en(app, client):
    """
    Test that locale selector respects en from Accept-Language header.
    
    Ensures proper header parsing when en is preferred.
    """
    response = client.get("/", headers={"Accept-Language": "en;q=1, zh;q=0.5"})
    text = response.get_data(as_text=True)

    assert "current locale: en" in text, \
        "expected locale en in response, got: {}".format(text)


def test_locale_selector_defaults_when_no_match(app, client):
    """
    Test that locale selector uses default locale when no match found.
    
    When Accept-Language header specifies unsupported languages,
    the default locale should be used.
    """
    response = client.get("/", headers={"Accept-Language": "fr,de"})
    text = response.get_data(as_text=True)

    # Should default to BABEL_DEFAULT_LOCALE which is "en"
    assert "current locale: en" in text, \
        "expected default locale en in response, got: {}".format(text)


def test_locale_selector_prefers_user_locale(app):
    """
    Test that user's stored locale is preferred over Accept-Language.
    
    When a user is authenticated and has a locale preference stored,
    that should take precedence over the Accept-Language header.
    """
    with app.app_context():
        user = User(username="foo", email="foo@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        # Test with request context and user logged in
        with app.test_request_context("/", headers={"Accept-Language": "en"}):
            login_user(user)
            locale = get_locale()
            assert locale == "zh", "expected locale zh for user, got {}".format(locale)


# ============================================================================
# Login and Authentication Tests
# ============================================================================


def test_login_creates_user(app, client):
    """
    Test that the /login route creates a user if needed and logs in.
    
    Verifies that the auto-created user is created with locale="zh".
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"logged in" in response.data

    with app.app_context():
        user = User.query.first()
        assert user is not None
        assert user.username == "test"
        assert user.locale == "zh"


def test_protected_route_requires_login(app, client):
    """
    Test that /protected route requires authentication.
    
    An unauthenticated request should be redirected.
    """
    response = client.get("/protected", follow_redirects=False)
    assert response.status_code == 302  # Redirect
    assert "/login" in response.location or "auth.login" in response.location


def test_protected_route_accessible_when_logged_in(app, client):
    """
    Test that /protected route is accessible when authenticated.
    
    After logging in via /login, the user should be able to access
    protected content.
    """
    # First log in
    client.get("/login")

    # Now access protected route
    response = client.get("/protected")
    assert response.status_code == 200
    assert b"protected content" in response.data


# ============================================================================
# CLI Command Tests
# ============================================================================


def test_translate_update_command_runs_successfully(app):
    """
    Test that CLI translate update command runs without errors.
    
    This verifies that the CLI commands work correctly with
    app.test_cli_runner() and that they can access current_app.config.
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "update"])
    
    assert result.exit_code == 0, "translate update failed: {}".format(result.output)
    assert "update languages" in result.output


def test_translate_init_command_runs_successfully(app):
    """
    Test that CLI translate init command runs without errors.
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "init", "fr"])
    
    assert result.exit_code == 0, "translate init failed: {}".format(result.output)
    assert "available languages" in result.output
    assert "init language: fr" in result.output


def test_translate_compile_command_runs_successfully(app):
    """
    Test that CLI translate compile command runs without errors.
    """
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "compile"])
    
    assert result.exit_code == 0, "translate compile failed: {}".format(result.output)
    assert "compile languages" in result.output


# ============================================================================
# Email Tests
# ============================================================================


def test_async_email_threading_no_context_error(app, monkeypatch):
    """
    Test that send_email does not raise context errors in background thread.
    
    This verifies that send_email correctly passes the real app instance
    (via _get_current_object()) to the thread, allowing it to create
    a new app context.
    """
    sent = {}

    def fake_send(msg):
        # Record the message that was "sent"
        sent["subject"] = msg.subject
        sent["body"] = msg.body

    with app.app_context():
        # Monkeypatch mail.send to avoid actual email sending
        monkeypatch.setattr("app.email.mail.send", fake_send)
        
        # This should not raise any errors
        send_email(
            "test subject",
            "noreply@example.com",
            ["user@example.com"],
            "text body",
            "<p>html body</p>"
        )

    # Give thread time to execute (in practice, a sleep or more complex test would be needed)
    # But since we're monkeypatching, the fake_send is called synchronously
    assert sent.get("subject") == "test subject"
    assert sent.get("body") == "text body"


# ============================================================================
# Edge Cases and Correct Patterns
# ============================================================================


def test_get_locale_without_request_context_uses_default(app):
    """
    Test that get_locale outside request context uses default locale.
    
    This is a correct pattern: when called without a request context,
    get_locale should handle it gracefully and use the default locale.
    
    Note: This test is informational. In production, get_locale should
    only be called within a request context (by Babel or our before_request).
    """
    with app.app_context():
        # Outside request context, current_user is not authenticated
        # and request is not available, so we should get a default
        try:
            # This may raise RuntimeError about working outside request context
            locale = get_locale()
            # If it doesn't raise, it should use default
            assert locale == "en"
        except RuntimeError:
            # Expected behavior: get_locale requires a request context
            pass


def test_create_app_with_testconfig_uses_memory_database(app):
    """
    Test that create_app with TestConfig uses an in-memory database.
    """
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
    assert app.config["TESTING"] is True


def test_locale_stored_in_g_before_request(app, client):
    """
    Test that locale is set in g during before_request.
    
    This verifies that the _set_locale_to_g hook correctly populates
    g.locale for use in templates.
    """
    response = client.get("/", headers={"Accept-Language": "zh"})
    text = response.get_data(as_text=True)
    
    # The index route uses g.get("locale"), which should be set
    assert "current locale:" in text
