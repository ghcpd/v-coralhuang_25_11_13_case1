import click
from flask import current_app


def register_cli(app):

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language (dummy implementation)."""
        # Ensure we have app context
        with app.app_context():
            langs = current_app.config["LANGUAGES"]
            click.echo("available languages: {}".format(langs))
            click.echo("init language: {}".format(lang))

    @translate.command()
    def update():
        """Update all languages (dummy implementation)."""
        with app.app_context():
            langs = current_app.config["LANGUAGES"]
            click.echo("update languages: {}".format(langs))

    @translate.command()
    def compile():
        """Compile all languages (dummy implementation)."""
        with app.app_context():
            langs = current_app.config["LANGUAGES"]
            click.echo("compile languages: {}".format(langs))
