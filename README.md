# Modular Flask Babel App

## Background
The original single-file Flask example mixed configuration, translations, CLI helpers, routing, and tests into one script. That suppressed key defects (missing multilingual defaults, Babel locale resolution issues, CLI commands requiring app contexts, and background email threads passing proxy objects), and the bundled tests contained learning anti-patterns that hid these flaws.

## Repair Strategy
1. **Configuration isolation** – Moved all settings into `config.py`, guaranteeing every environment provides `LANGUAGES`, Babel defaults, and mail parameters.
2. **Modular app factory** – Split functionality into `app/__init__.py`, `models.py`, `routes.py`, `cli.py`, and `email.py`, ensuring Babel and Flask extensions initialize cleanly, `get_locale` respects user preferences vs Accept-Language, and async emails receive a real app instance.
3. **Realistic tests** – Replaced the broken pytest suite with scoped fixtures, request-context-aware helper tests, and new assertions covering localization, CLI command execution, and async email threads.
4. **Automation & docs** – Added `requirements.txt`, Docker support, shell scripts, and a README so anyone can reproduce setup and run tests end-to-end.

## Repository Layout
```
.
├── app/
│   ├── __init__.py        # Application factory, Babel locale selector, login configuration
│   ├── cli.py             # Translation CLI helpers using Flask CLI + with_appcontext
│   ├── email.py           # Thread-safe async email helpers passing real app
│   ├── models.py          # SQLAlchemy + User definition
│   └── routes.py          # Basic routes for index, login, protected view
├── config.py              # Base/Dev/Test configs with LANGUAGES + Babel defaults
├── translations/zh/LC_MESSAGES/messages.po
├── requirements.txt
├── setup.sh
├── run_test.sh
├── run_test.bat
├── Dockerfile
├── tests/
│   └── test_app.py        # Pytest coverage for i18n, CLI, async email, login behavior
└── README.md
```

## Setup & Testing
1. **Linux/macOS** – Run `./setup.sh` to detect the OS, (re)create `.venv`, and install dependencies. `setup.sh` is idempotent.
2. **Linux/macOS** – Invoke `./run_test.sh` to activate `.venv` and execute `pytest`. `run_test.sh` exits if `.venv` is missing.
3. **Windows** – Use `.venv\Scripts\activate` (after manually creating the venv) and run `pytest`, or simply execute `run_test.bat` once `.venv` exists.
4. **Docker** – `docker build -t flask-app .` and `docker run --rm flask-app` will install deps inside the container and run all tests.

## Known Limitations & Next Steps
- The translation catalog is minimal (only the login message). Running `pybabel extract`/`init`/`update` would be required for full coverage.
- Email sending still relies on an SMTP server configured in `MAIL_*`; tests monkeypatch `mail.send` rather than connecting to an actual server.
- The default locale data and login behavior assume only `en`/`zh`; additional locales would require updates to `translations/`.

