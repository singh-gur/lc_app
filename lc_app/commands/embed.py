from typing import Literal

import click

from lc_app.core.rag import embed_csv_data, embed_web_data


@click.command()
@click.option(
    "--doctype", type=click.Choice(["csv", "web"]), help="Type of the document."
)
@click.option("--db-path", type=str, help="Path to the database.", envvar="DB_PATH")
@click.option(
    "--embed-model", type=str, help="Embedding model to use.", envvar="EMBED_MODEL"
)
@click.option("--doc", type=str, required=False, help="Path to the documents.")
@click.option(
    "--url", type=str, multiple=True, required=False, help="Path to web urls."
)
@click.option("--scrape-class", type=str, required=False, help="CSS class to scrape.")
def embed(
    doctype: Literal["csv", "web"],
    db_path: str,
    embed_model: str | None = None,
    doc: str | None = None,
    url: list[str] | None = None,
    scrape_class: str | None = None,
):
    """Embed documents using Ollama and store them in the chroma database."""
    click.echo(f"Embedding documents from: {doc}")

    if doctype == "csv":
        click.echo("Document type is CSV.")
        if doc is None:
            click.echo("No document path provided for CSV.")
            return
        embed_csv_data(file_path=doc, chroma_db_path=db_path, model=embed_model)
    elif doctype == "web":
        click.echo("Document type is Web.")
        if url is None:
            click.echo("No URL provided for web data.")
            return
        embed_web_data(
            urls=url,
            chroma_db_path=db_path,
            webpage_class=scrape_class,
            model=embed_model,
        )
    else:
        click.echo("Unsupported document type.")
        return
    click.echo(f"Documents embedded and stored in: {db_path}")
    click.echo("Embedding completed successfully.")
    click.echo("You can now use the 'ask' command to query the embedded data.")
    return
