# Flask App - Refactored

This repository refactors a single-file Flask app into a modular structure, fixes configuration and localization bugs, and provides a reproducible test environment.

What I fixed:
- Moved application into modules: `app`, `config.py`, and `tests`.
- Ensured i18n config options (`LANGUAGES`, `BABEL_DEFAULT_LOCALE`, `BABEL_DEFAULT_TIMEZONE`) are defined in `BaseConfig`.
- Implemented robust `get_locale()` function with request context awareness and user locale precedence.
- Ensured `login_manager` uses dynamic login view and messages.
- Fixed async email thread to pass real app instance via `current_app._get_current_object()`.
- Made CLI commands safe to run via `app.test_cli_runner()`.
- Added tests that verify locale selection, login messages via flashed messages, CLI commands, and async email sending.

How to run:
- Run `setup.sh` (Linux/macOS) or on Windows use the PowerShell equivalent to create a virtual environment and install dependencies.
- Run tests with `pytest` directly or `run_test.sh`/`run_test.bat`.

Known limitations:
- Full gettext PO/MO translation files are not included; a trivial monkeypatch is used in tests to simulate translation behavior.

