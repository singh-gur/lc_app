from typing import Literal

import click

from lc_app.core.rag import embed_csv_data, embed_web_data, embed_json_data
from tempfile import NamedTemporaryFile
from lc_app.core.scrapers.models import Article, DataSet
from lc_app.core.scrapers.yf_scraper import YahooFinanceNewsScraper
from json import dumps
from pydantic.json import pydantic_encoder

@click.group()
def embed():
    """CLI for embedding documents."""
    pass


@embed.command()
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
def raw(
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


@embed.command()
@click.option(
    "--db-path", type=str, required=True, help="Path to the database.", envvar="DB_PATH"
)
@click.option("--ticker", type=str, required=False, help="Ticker symbol.")
@click.option(
    "--topic", type=str, required=False, help="Topic to scrape news articles for."
)
@click.option(
    "--source", type=str, required=False, default="yahoo", help="Source of the data."
)
@click.option(
    "--embed-model",
    type=str,
    required=False,
    help="Embedding model to use.",
    envvar="EMBED_MODEL",
)
@click.option(
    "--ollama-host",
    type=str,
    required=False,
    help="Ollama host URL.",
    envvar="OLLAMA_HOST",
)
def news(
    db_path: str,
    ticker: str | None = None,
    topic: str | None = None,
    source: str | None = "yahoo",
    embed_model: str | None = None,
    ollama_host: str | None = None,
):
    """Embed news articles for a given ticker symbol."""
    click.echo(f"Embedding news articles for ticker: {ticker}")

    articles: list[Article] = []
    if source == "yahoo":
        click.echo("Scraping news articles from Yahoo Finance.")
        scraper = YahooFinanceNewsScraper(ticker=ticker, topic=topic)
    else:
        click.echo("Unsupported source.")
        return

    articles = scraper.sync_scrape()
    if not articles:
        click.echo("No articles found.")
        return
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(DataSet[Article](entries=articles).model_dump_json().encode())
        temp_file.flush()
        temp_file.seek(0)
        temp_file_path = temp_file.name
        embed_json_data(file_path=temp_file_path, chroma_db_path=db_path, model=embed_model)
    click.echo(f"Articles embedded and stored in: {db_path}")
    click.echo("Embedding completed successfully.")
    click.echo("You can now use the 'ask' command to query the embedded data.")
    return
