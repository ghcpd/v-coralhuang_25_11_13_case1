import os


class BaseConfig(object):
    """Base config without i18n config."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dummy-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    # i18n defaults
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


class DevConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    # For deterministic tests, set default locale to zh
    BABEL_DEFAULT_LOCALE = "zh"
    LANGUAGES = ["en", "zh"]
    # Simple translation mapping for tests
    TRANSLATIONS = {"zh": {"Please log in to access this page.": "[ZH_LOGIN_MESSAGE]"}}
