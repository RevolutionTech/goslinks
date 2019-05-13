import click
from flask.cli import with_appcontext

from goslinks.db.factory import get_model


@click.command()
@with_appcontext
def migrate():
    """Creates and migrates database tables."""
    for model_name in ("user", "link"):
        model = get_model(model_name)
        click.echo(f"Creating table {model.Meta.table_name}... ", nl=False)
        try:
            model.create_table()
        except Exception:
            click.echo(click.style("FAILED!", fg="red"))
            raise
        else:
            click.echo(click.style("SUCCESS!", fg="green"))
