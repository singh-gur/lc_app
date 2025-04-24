import pandas as pd
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM

OLLAMA_HOST = "http://192.168.2.110:11434"  # Ollama server URL
# Load CSV market data with Pandas


def run_rag_chain(
    data: pd.DataFrame,
    query: str,
    ollama_host: str = OLLAMA_HOST,
    search_kwargs: dict = {"k": 5},
) -> tuple:
    loader = DataFrameLoader(data)
    docs = loader.load()
    # Initialize Ollama embeddings and LLM
    embeddings = OllamaEmbeddings(base_url=ollama_host, model="nomic-embed-text")
    llm = OllamaLLM(
        base_url=ollama_host, model="deepseek-r1:14b"
    )  # Updated to use langchain-ollama package

    # Create Chroma vector database from documents
    db = Chroma.from_documents(docs, embeddings)

    # Create RAG chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs=search_kwargs),
        return_source_documents=True,
    )

    """Run the RAG chain with the given query."""
    response = rag_chain.invoke(query)
    return response["result"], response["source_documents"]
