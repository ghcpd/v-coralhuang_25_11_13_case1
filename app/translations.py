from flask import current_app, request, has_request_context
from flask_login import current_user


def get_locale():
    # If user is authenticated and has a preferred locale, use it
    try:
        if current_user.is_authenticated and current_user.locale:
            return current_user.locale
    except Exception:
        # current_user may not be available outside request context
        pass

    # When there is no request context, use config default
    if not has_request_context():
        return current_app.config.get("BABEL_DEFAULT_LOCALE")

    # Fall back to Accept-Language header
    languages = current_app.config.get("LANGUAGES", ["en"])
    best = request.accept_languages.best_match(languages)
    return best or current_app.config.get("BABEL_DEFAULT_LOCALE")
