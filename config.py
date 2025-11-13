import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


class BaseConfig:
    """Shared configuration settings with defaults for i18n."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dummy-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    BABEL_TRANSLATION_DIRECTORIES = str(ROOT_DIR / "translations")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 25))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")


class DevConfig(BaseConfig):
    """Development config with verbose logging."""

    DEBUG = True


class TestConfig(BaseConfig):
    """Testing configuration with in-memory database support."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
