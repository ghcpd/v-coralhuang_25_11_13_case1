import pytest

from flask_login import login_user

from app import create_app, db, get_locale
from app.email import mail, send_email
from app.models import User
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_testconfig_should_provide_languages(app):
    assert "LANGUAGES" in app.config
    assert isinstance(app.config["LANGUAGES"], (list, tuple))
    assert "en" in app.config["LANGUAGES"]


def test_locale_selector_respects_accept_language(app, client):
    response = client.get("/", headers={"Accept-Language": "zh;q=1, en;q=0.5"})
    assert "current locale: zh" in response.get_data(as_text=True)


def test_locale_selector_prefers_user_locale(app):
    with app.app_context():
        user = User(username="foo", email="foo@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context("/"):
            login_user(user)
            assert get_locale() == "zh"


def test_login_required_message_localized(app, client):
    response = client.get("/protected", headers={"Accept-Language": "zh"}, follow_redirects=True)
    text = response.get_data(as_text=True)
    assert "请登录以访问此页面。" in text
    assert "Please log in to access this page." not in text


def test_async_email_uses_app_context(app, monkeypatch):
    sent = {}

    class ImmediateThread:
        def __init__(self, target=None, args=(), kwargs=None):
            self.target = target
            self.args = args or ()
            self.kwargs = kwargs or {}

        def start(self):
            self.target(*self.args, **self.kwargs)

    def fake_send(msg):
        sent["subject"] = msg.subject

    with app.app_context():
        monkeypatch.setattr(mail, "send", fake_send)
        monkeypatch.setattr("app.email.threading.Thread", ImmediateThread)
        send_email("subject", "noreply@example.com", ["user@example.com"], "text", "<p>html</p>")

    assert sent.get("subject") == "subject"


def test_translate_compile_command_runs_without_manual_context(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "compile"])
    assert result.exit_code == 0
    assert "compile languages" in result.output


def test_get_locale_returns_user_preference(app):
    with app.app_context():
        user = User(username="bar", email="bar@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context("/", headers={"Accept-Language": "en"}):
            login_user(user)
            assert get_locale() == "zh"
