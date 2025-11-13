"""
Locale selection logic for Babel.
"""

from flask import current_app, request, g
from flask_login import current_user


def get_locale():
    """
    Select the best locale for the current request.
    
    Precedence:
    1. User's stored locale (if authenticated)
    2. Best match from Accept-Language header
    3. Default locale from config
    
    This function is registered as Babel's locale selector.
    It is called during request handling (within request context).
    
    Returns:
        str: Selected locale code (e.g., 'en', 'zh')
    """
    # If user is authenticated and has a locale preference, use it
    try:
        if current_user and current_user.is_authenticated and current_user.locale:
            return current_user.locale
    except (RuntimeError, AttributeError):
        # RuntimeError: working outside of request context
        # AttributeError: current_user is None outside request context
        pass

    # Otherwise, use the best match from Accept-Language header
    languages = current_app.config.get("LANGUAGES", [])
    if not languages:
        return current_app.config.get("BABEL_DEFAULT_LOCALE", "en")
    
    try:
        matched = request.accept_languages.best_match(languages)
        if matched:
            return matched
    except RuntimeError:
        # RuntimeError: working outside of request context
        pass
    
    # Fallback to default locale
    return current_app.config.get("BABEL_DEFAULT_LOCALE", "en")
