import os
import threading

from flask import Flask, current_app, g, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    UserMixin,
)
from flask_mail import Mail, Message
from flask_babel import Babel, gettext, lazy_gettext as _l
import click


class BaseConfig(object):
    """Base config without i18n config."""

    SECRET_KEY = "dummy-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class DevConfig(BaseConfig):
    """Development config with full i18n options."""

    DEBUG = True
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


class TestConfig(BaseConfig):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()

login_manager.login_view = "auth.login"
login_manager.login_message = _l("Please log in to access this page.")


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    locale = db.Column(db.String(8), default=None)

    def __repr__(self):
        return "<User {}>".format(self.username)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    register_basic_routes(app)

    register_cli(app)


    @app.before_request
    def _set_locale_to_g():
        g.locale = get_locale()


    if not app.debug and not app.testing:
        pass

    return app



@babel.localeselector
def get_locale():


    if current_user.is_authenticated and current_user.locale:
        return current_user.locale

    languages = current_app.config["LANGUAGES"]
    return request.accept_languages.best_match(languages)



def register_basic_routes(app):

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
        login_user(user)
        return "logged in"


def register_cli(app):


    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("available languages: {}".format(langs))
        click.echo("init language: {}".format(lang))

    @translate.command()
    def update():
        """Update all languages (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("update languages: {}".format(langs))

    @translate.command()
    def compile():
        """Compile all languages (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("compile languages: {}".format(langs))



def send_async_email(app, msg):

    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    threading.Thread(target=send_async_email, args=(current_app, msg)).start()




import pytest


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

    assert "LANGUAGES" in app.config, "LANGUAGES missing in TestConfig"
    assert isinstance(app.config["LANGUAGES"], (list, tuple)), "LANGUAGES should be list/tuple"
    assert "en" in app.config["LANGUAGES"]


def test_locale_selector_respects_accept_language(app, client):

    response = client.get("/", headers={"Accept-Language": "zh;q=1, en;q=0.5"})
    text = response.get_data(as_text=True)


    assert "current locale: zh" in text, "expected locale zh in response, got: {}".format(text)


def test_login_message_translated_for_zh(app, client):

    response = client.get(
        "/protected",
        headers={"Accept-Language": "zh"},
        follow_redirects=True,
    )
    text = response.get_data(as_text=True)


    expected_zh_placeholder = "[ZH_LOGIN_MESSAGE]"
    assert expected_zh_placeholder in text, "expected zh login message placeholder in response"
    assert "Please log in to access this page." not in text


def test_locale_selector_prefers_user_locale(app):

    with app.app_context():
        user = User(username="foo", email="foo@example.com", locale="zh")
        db.session.add(user)
        db.session.commit()

        with app.test_request_context("/"):
            login_user(user)
            locale = get_locale()
            assert locale == "zh", "expected locale zh for user, got {}".format(locale)


def test_async_email_uses_correct_locale(app, monkeypatch):
    sent = {}

    def fake_send(msg):
        sent["subject"] = msg.subject

    with app.app_context():
        monkeypatch.setattr(mail, "send", fake_send)
        send_email("subject", "noreply@example.com", ["user@example.com"], "text", "<p>html</p>")

    assert sent.get("subject") == "subject"


def test_translate_update_command_can_run_without_current_app(app):

    runner = app.test_cli_runner()
    result = runner.invoke(args=["translate", "update"])
    assert result.exit_code == 0, result.output


def test_bad_call_locale_selector_without_request_context(app):
    locale = get_locale()

    assert locale == "zh"


def test_bad_use_global_app_without_fixture():
    global_app = create_app() 
    client = global_app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
