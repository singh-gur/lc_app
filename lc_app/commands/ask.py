import click

from lc_app.core.rag import run_rag_chain


@click.command()
@click.option(
    "--query", type=str, prompt="Enter your query", help="The query you want to ask."
)
@click.option("--db-path", type=str, help="Path to the database.")
def ask(query: str, db_path: str):
    """Ask a question using the RAG chain."""
    click.echo(f"Loading documents from: {db_path}")
    click.echo(f"You asked: {query}")
    answer, source_docs = run_rag_chain(db_path, query)
    click.echo(f"Answer: {answer}")
    click.echo(f"Source documents: {source_docs}")
    return
