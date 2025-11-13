class BaseConfig(object):
    """Base config with sane i18n defaults."""

    SECRET_KEY = "dummy-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

    # Internationalization defaults
    LANGUAGES = ["en"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


class DevConfig(BaseConfig):
    """Development config with extra languages available."""

    DEBUG = True
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


class TestConfig(BaseConfig):
    """Test configuration uses in-memory sqlite and zh as default locale for tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False

    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "zh"
    BABEL_DEFAULT_TIMEZONE = "UTC"
