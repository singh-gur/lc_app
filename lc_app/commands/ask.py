import click

from lc_app.core.rag import run_rag_chain


@click.command()
@click.option(
    "--query", type=str, prompt="Enter your query", help="The query you want to ask."
)
@click.option("--docs", type=str, help="Path to the documents.")
def ask(query: str, docs: str):
    click.echo(f"You asked: {query}")
    (answer, source_docs) = run_rag_chain(docs, query)
    click.echo(f"Answer: {answer}")
    click.echo(f"Source documents: {source_docs}")
