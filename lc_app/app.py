import click

from lc_app.commands import add_commands


@click.group()
def cli():
    """A starter CLI application."""
    pass


def run():
    """Run the CLI application."""
    add_commands(cli)
    cli(prog_name="lc_app", standalone_mode=False)
