"""
CLI commands for translation and localization.
"""

import click
from flask import current_app


def register_cli(app):
    """
    Register CLI command groups.
    
    All CLI commands access current_app.config, which works correctly
    within the Flask app context (automatically provided by test_cli_runner).
    """

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("available languages: {}".format(langs))
        click.echo("init language: {}".format(lang))

    @translate.command()
    def update():
        """Update all languages (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("update languages: {}".format(langs))

    @translate.command()
    def compile():
        """Compile all languages (dummy implementation)."""
        langs = current_app.config["LANGUAGES"]
        click.echo("compile languages: {}".format(langs))
