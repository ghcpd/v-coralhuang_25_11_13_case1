"""
Application configuration classes.

Defines BaseConfig, DevConfig, and TestConfig with proper
multilingual settings for Babel.
"""


class BaseConfig(object):
    """Base config with common i18n settings."""

    SECRET_KEY = "dummy-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    # Common multilingual settings
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


class DevConfig(BaseConfig):
    """Development config with debugging enabled."""

    DEBUG = True


class TestConfig(BaseConfig):
    """Test config with in-memory database and CSRF disabled."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
