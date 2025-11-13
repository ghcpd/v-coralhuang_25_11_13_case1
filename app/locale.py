from flask import current_app, request
from flask_login import current_user


def get_locale():
    """Return a locale string.

    Precedence:
    1) The logged-in user's explicit locale
    2) The request Accept-Language best match
    3) App default locale
    """
    # 1) user preference if set
    try:
        # Use getattr to avoid AttributeError if current_user is not a proxy with expected attributes
        if getattr(current_user, "is_authenticated", False) and getattr(current_user, "locale", None):
            return current_user.locale
    except Exception:
        # no user context (e.g. outside request) — fall through to default
        pass

    # 2) Accept-Language header if in a request context
    try:
        languages = current_app.config.get("LANGUAGES", ["en"])
        return request.accept_languages.best_match(languages) or current_app.config.get(
            "BABEL_DEFAULT_LOCALE", "en"
        )
    except RuntimeError:
        # no request context — return the app default
        return current_app.config.get("BABEL_DEFAULT_LOCALE", "en")
