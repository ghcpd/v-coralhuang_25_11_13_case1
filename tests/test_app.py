from flask import current_app
from app import db
from app.models import User
from app.email import send_email
from flask_babel import gettext, lazy_gettext as _l
import pytest
from app import create_app



def test_testconfig_should_provide_languages(app):
    assert "LANGUAGES" in app.config
    assert isinstance(app.config["LANGUAGES"], (list, tuple))
    assert "en" in app.config["LANGUAGES"]


def test_locale_selector_respects_accept_language(app, client):
    response = client.get("/", headers={"Accept-Language": "zh;q=1, en;q=0.5"})
    text = response.get_data(as_text=True)

    assert "current locale: zh" in text


def test_login_message_translated_for_zh(app, client):
    # The TestConfig includes a small TRANSLATIONS mapping that maps English to a zh placeholder.
    response = client.get(
        "/protected",
        headers={"Accept-Language": "zh"},
        follow_redirects=True,
    )
    text = response.get_data(as_text=True)
    # the login route renders flashed messages; check that our config-mapped translation is present
    assert "[ZH_LOGIN_MESSAGE]" in text
    assert "Please log in to access this page." not in text



def test_locale_selector_prefers_user_locale(app, client):
    with app.app_context():
        user = User(username="foo", email="foo@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        # Use request context and login the user
        with app.test_request_context("/"):
            from flask_login import login_user

            login_user(user)
            from app.translations import get_locale

            locale = get_locale()
            assert locale == "zh"



def test_async_email_uses_correct_locale(app, monkeypatch):
    sent = {}

    def fake_send(msg):
        sent["subject"] = msg.subject

    with app.app_context():
        import app.email as email_mod
        monkeypatch.setattr(email_mod.mail, "send", fake_send)
        # This will start a thread that uses the app._get_current_object() context
        send_email("subject", "noreply@example.com", ["user@example.com"], "text", "<p>html</p>")

    assert sent.get("subject") == "subject"



def test_translate_update_command_can_run_without_current_app(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "update"])
    assert result.exit_code == 0, result.output



def test_bad_call_locale_selector_without_request_context(app):
    # calling get_locale outside of a request context should not raise and should return default
    from app.translations import get_locale

    locale = get_locale()
    assert locale == app.config.get("BABEL_DEFAULT_LOCALE")



def test_bad_use_global_app_without_fixture():
    global_app = create_app()
    client = global_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
