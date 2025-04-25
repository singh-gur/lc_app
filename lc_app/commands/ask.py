import click

from lc_app.core.rag import run_rag_chain


@click.command()
@click.option(
    "--query", type=str, prompt="Enter your query", help="The query you want to ask."
)
@click.option("--db-path", type=str, help="Path to the database.", envvar="DB_PATH")
@click.option(
    "--embed-model",
    type=str,
    help="Embedding model to use.",
    required=False,
    envvar="EMBED_MODEL",
)
@click.option(
    "--rag-model",
    type=str,
    help="RAG model to use.",
    required=False,
    envvar="RAG_MODEL",
)
def ask(
    query: str,
    db_path: str,
    embed_model: str | None = None,
    rag_model: str | None = None,
):
    """Ask a question using the RAG chain."""
    click.echo(f"Loading documents from: {db_path}")
    click.echo(f"You asked: {query}")
    answer, _ = run_rag_chain(
        db_path=db_path, query=query, embedding_model=embed_model, llm_model=rag_model
    )
    click.echo(f"Answer: {answer}")
    return
