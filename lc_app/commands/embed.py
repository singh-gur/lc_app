import click

from lc_app.core.rag import embed_csv_data


@click.command()
@click.option("--doc", type=str, help="Path to the documents.")
@click.option("--db-path", type=str, help="Path to the database.", envvar="DB_PATH")
@click.option(
    "--embed-model", type=str, help="Embedding model to use.", envvar="EMBED_MODEL"
)
def embed(doc: str, db_path: str, embed_model: str | None = None):
    """Embed documents using Ollama and store them in the chroma database."""
    click.echo(f"Embedding documents from: {doc}")
    embed_csv_data(file_path=doc, chroma_db_path=db_path, embed_model=embed_model)
    click.echo(f"Documents embedded and stored in: {db_path}")
    click.echo("Embedding completed successfully.")
    click.echo("You can now use the 'ask' command to query the embedded data.")
    return
