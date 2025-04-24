from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM

OLLAMA_HOST = "http://192.168.2.110:11434"  # Ollama server URL
# Load CSV market data with Pandas


def embed_csv_data(file_path: str, chroma_db_path: str) -> None:
    """Load CSV data and create embeddings using Ollama."""
    loader = CSVLoader(file_path)
    docs = loader.load()

    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(base_url=OLLAMA_HOST, model="nomic-embed-text")

    # Create Chroma vector database from documents
    Chroma.from_documents(docs, embeddings, persist_directory=chroma_db_path)


def run_rag_chain(
    db_path: str,
    query: str,
    ollama_host: str = OLLAMA_HOST,
    search_kwargs: dict = {"k": 5},
) -> tuple:
    db = Chroma(
        persist_directory=db_path,
        embedding_function=OllamaEmbeddings(
            base_url=ollama_host, model="nomic-embed-text"
        ),
    )

    llm = OllamaLLM(
        base_url=ollama_host, model="deepseek-r1:14b"
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
