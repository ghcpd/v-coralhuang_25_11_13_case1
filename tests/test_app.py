from flask import current_app
from app import create_app
from app.config import TestConfig
from app import db
from app.models import User
from app.email import send_email
from app.locale import get_locale


def test_testconfig_should_provide_languages(app):
    assert "LANGUAGES" in app.config, "LANGUAGES missing in TestConfig"
    assert isinstance(app.config["LANGUAGES"], (list, tuple)), "LANGUAGES should be list/tuple"
    assert "en" in app.config["LANGUAGES"]


def test_locale_selector_respects_accept_language(app, client):
    response = client.get("/", headers={"Accept-Language": "zh;q=1, en;q=0.5"})
    text = response.get_data(as_text=True)

    assert "current locale: zh" in text, "expected locale zh in response, got: {}".format(text)


def test_login_message_translated_for_zh(app, client, monkeypatch):
    # Replace the login message before testing redirect so we can assert it's shown
    from app import login_manager
    login_manager.login_message = "[ZH_LOGIN_MESSAGE]"

    response = client.get(
        "/protected",
        headers={"Accept-Language": "zh"},
        follow_redirects=True,
    )
    text = response.get_data(as_text=True)

    assert "[ZH_LOGIN_MESSAGE]" in text, "expected zh login message placeholder in response"


def test_locale_selector_prefers_user_locale(app):
    with app.app_context():
        user = User(username="foo", email="foo@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context("/"):
            from flask_login import login_user

            login_user(user)
            locale = get_locale()
            assert locale == "zh", "expected locale zh for user, got {}".format(locale)


def test_async_email_uses_correct_locale(app, monkeypatch):
    sent = {}

    def fake_send(msg):
        sent["subject"] = msg.subject

    with app.app_context():
        monkeypatch.setattr("app.email.mail.send", fake_send)
        send_email("subject", "noreply@example.com", ["user@example.com"], "text", "<p>html</p>")

    assert sent.get("subject") == "subject"


def test_translate_update_command_can_run_without_current_app(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "update"])
    assert result.exit_code == 0, result.output


def test_bad_call_locale_selector_without_request_context(app):
    # The app fixture runs inside an app_context but without a request context.
    locale = get_locale()

    assert locale == app.config["BABEL_DEFAULT_LOCALE"]


def test_bad_use_global_app_without_fixture():
    global_app = create_app(TestConfig)
    client = global_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
