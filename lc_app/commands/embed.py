import click

from lc_app.core.rag import embed_csv_data


@click.command()
@click.option("--doc", type=str, help="Path to the documents.")
@click.option("--db-path", type=str, help="Path to the database.")
def embed(doc: str, db_path: str):
    click.echo(f"Embedding documents from: {doc}")
    embed_csv_data(doc, db_path)
    click.echo(f"Documents embedded and stored in: {db_path}")
    click.echo("Embedding completed successfully.")
    click.echo("You can now use the 'ask' command to query the embedded data.")
    return
