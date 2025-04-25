from os import getenv

from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM

DEFAULT_OLLAMA_HOST = "http://localhost:11434"  # Ollama server URL
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"  # Default embedding model
DEFAULT_RAG_MODEL = "deepseek-r1:14b"  # Default RAG model
# Load CSV market data with Pandas


def embed_csv_data(
    file_path: str,
    chroma_db_path: str,
    ollama_host: str | None = None,
    model: str | None = None,
) -> None:
    """Load CSV data and create embeddings using Ollama."""

    if ollama_host is None:
        ollama_host = getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    if model is None:
        model = DEFAULT_EMBEDDING_MODEL

    loader = CSVLoader(file_path)
    docs = loader.load()

    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(base_url=ollama_host, model=model)

    # Create Chroma vector database from documents
    Chroma.from_documents(docs, embeddings, persist_directory=chroma_db_path)


def run_rag_chain(
    db_path: str,
    query: str,
    ollama_host: str | None = None,
    search_kwargs: dict = {"k": 5},
    embedding_model: str | None = None,
    llm_model: str | None = None,
) -> tuple:
    """Run the RAG chain with the given query and return the answer and source documents."""
    if ollama_host is None:
        ollama_host = getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    if embedding_model is None:
        embedding_model = DEFAULT_EMBEDDING_MODEL

    if llm_model is None:
        llm_model = DEFAULT_RAG_MODEL

    # Initialize Chroma vector database
    db = Chroma(
        persist_directory=db_path,
        embedding_function=OllamaEmbeddings(
            base_url=ollama_host, model=embedding_model
        ),
    )

    llm = OllamaLLM(
        base_url=ollama_host, model=llm_model
    )  # Updated to use langchain-ollama package

    # Create RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs=search_kwargs),
        return_source_documents=True,
    )

    """Run the RAG chain with the given query."""
    response = rag_chain.invoke(query)
    return response["result"], response["source_documents"]
