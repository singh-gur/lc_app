from os import getenv

from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    AsyncChromiumLoader,
    CSVLoader,
    JSONLoader,
)
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langfuse.callback import CallbackHandler

DEFAULT_LANFUSE_HOST = "https://langfuse.gsingh.io"  # Langfuse server URL
DEFAULT_OLLAMA_HOST = "http://localhost:11434"  # Ollama server URL
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"  # Default embedding model
DEFAULT_RAG_MODEL = "deepseek-r1:7b"  # Default RAG model
DEFAULT_CHUNK_SIZE = 1000  # Default chunk size for text splitting
DEFAULT_CHUNK_OVERLAP = 200  # Default chunk overlap for text splitting
DEFAULT_WEB_CLASS = "article"  # Default CSS class for web scraping
# Load CSV market data with Pandas


def embed_web_data(
    urls: list[str],
    chroma_db_path: str,
    webpage_class: str | None = None,
    ollama_host: str | None = None,
    model: str | None = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> None:
    """Load web data and create embeddings using Ollama."""

    if ollama_host is None:
        ollama_host = getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    if model is None:
        model = getenv("EMBED_MODEL", DEFAULT_EMBEDDING_MODEL)

    if webpage_class is None:
        webpage_class = DEFAULT_WEB_CLASS

    loader = AsyncChromiumLoader(urls)
    html_docs = loader.load()

    transformer = BeautifulSoupTransformer()

    docs_transformed = transformer.transform_documents(
        html_docs, tags_to_extract=["article"]
    )

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )

    split_docs = text_splitter.split_documents(docs_transformed)

    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(base_url=ollama_host, model=model)

    if split_docs:
        # Create Chroma vector database from documents
        Chroma.from_documents(split_docs, embeddings, persist_directory=chroma_db_path)


def embed_json_data(
    file_path: str,
    chroma_db_path: str,
    ollama_host: str | None = None,
    model: str | None = None,
) -> None:
    """Load JSON data and create embeddings using Ollama."""

    # FIXME: add jq schema to parse JSON
    loader = JSONLoader(file_path, jq_schema=".entries[]", text_content=False)
    docs = loader.load()

    embed_from_documents(docs, chroma_db_path, ollama_host, model)


def embed_csv_data(
    file_path: str,
    chroma_db_path: str,
    ollama_host: str | None = None,
    model: str | None = None,
) -> None:
    """Load CSV data and create embeddings using Ollama."""

    loader = CSVLoader(file_path)
    docs = loader.load()

    embed_from_documents(docs, chroma_db_path, ollama_host, model)


def embed_from_documents(
    docs: list[Document],
    chroma_db_path: str,
    ollama_host: str | None = None,
    model: str | None = None,
) -> None:
    """Embed documents and store them in the Chroma database."""
    if ollama_host is None:
        ollama_host = getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    if model is None:
        model = getenv("EMBED_MODEL", DEFAULT_EMBEDDING_MODEL)

    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(base_url=ollama_host, model=model)

    # Create Chroma vector database from documents
    Chroma.from_documents(docs, embeddings, persist_directory=chroma_db_path)


def embed_from_texts(
    data: list[str],
    chroma_db_path: str,
    ollama_host: str | None = None,
    model: str | None = None,
) -> None:
    """Load text data and create embeddings using Ollama."""

    if ollama_host is None:
        ollama_host = getenv("OLLAMA_HOST", DEFAULT_OLLAMA_HOST)

    if model is None:
        model = getenv("EMBED_MODEL", DEFAULT_EMBEDDING_MODEL)

    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(base_url=ollama_host, model=model)

    # Create Chroma vector database from documents
    Chroma.from_texts(data, embeddings, persist_directory=chroma_db_path)


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
        embedding_model = getenv("EMBED_MODEL", DEFAULT_EMBEDDING_MODEL)

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

    langfuse_callback = get_langfuse_callback_handler()
    config = {}
    if langfuse_callback is not None:
        config["callbacks"] = [langfuse_callback]
    """Run the RAG chain with the given query."""
    response = rag_chain.invoke(query, config=config)
    return response["result"], response["source_documents"]


def get_langfuse_callback_handler() -> CallbackHandler | None:
    """Get the Langfuse callback handler for tracking RAG chain runs."""
    langfuse_host = getenv("LANGFUSE_HOST", DEFAULT_LANFUSE_HOST)

    public_key = getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = getenv("LANGFUSE_SECRET_KEY")
    if public_key is None or secret_key is None:
        return None

    return CallbackHandler(
        public_key=public_key,
        secret_key=secret_key,
        host=langfuse_host,
    )
