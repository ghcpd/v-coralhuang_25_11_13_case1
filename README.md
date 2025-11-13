# Flask i18n Fix & Tests

This repository contains a Flask app refactored into a package with proper i18n configuration, CLI commands, email sending, and tests. It was refactored to address several issues:

- Ensure `LANGUAGES` and `BABEL_DEFAULT_LOCALE/TIMEZONE` are correctly defined in our config hierarchy.
- Fix Babel locale selection behavior (user locale -> accept-language -> app default).
- Avoid using `current_app` in CLI functions; register CLI commands with the app instance.
- Pass a real Flask app object to background email threads via `_get_current_object()`.
- Provide a modular project layout for easier testing and maintainability.

Usage:
- Setup on Unix/macOS: `./setup.sh` then `./run_test.sh`.
- Setup on Windows: run `run_test.bat` (after creating a venv and installing the requirements).
- Docker: `docker build -t flask-i18n . && docker run --rm flask-i18n`


Tests validate:
- TestConfig provides LANGUAGES and default locale.
- Babel locale selection from Accept-Language and user preference.
- login_required flashed messages show up on redirect.
- CLI translate update command runs with `test_cli_runner()`.
- Asynchronous email uses mail.send with passed-in app instance.

Limitations and future improvements:
- There's no actual gettext translation files in this simplified project; tests monkeypatch `gettext` to validate translation flow.
- Email and migration behavior is lightweight and meant for testing; integration with real mail server and migration flow would need extra work.
