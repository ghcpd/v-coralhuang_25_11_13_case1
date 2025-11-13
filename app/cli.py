import click

from flask import current_app
from flask.cli import with_appcontext


def register_cli(app):
    """Register translation helpers that rely on the application configuration."""

    @app.cli.group("translate")
    def translate():
        """Manage translation files."""

    @translate.command("init")
    @with_appcontext
    def init_command():
        langs = current_app.config["LANGUAGES"]
        click.echo(f"init languages: {langs}")

    @translate.command("update")
    @with_appcontext
    def update_command():
        langs = current_app.config["LANGUAGES"]
        click.echo(f"update languages: {langs}")

    @translate.command("compile")
    @with_appcontext
    def compile_command():
        langs = current_app.config["LANGUAGES"]
        click.echo(f"compile languages: {langs}")
