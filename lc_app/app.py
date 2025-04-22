import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load CSV market data with Pandas
df = pd.read_csv('./data/dummy_market_data.csv')

# Optional: Select relevant columns
selected_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
df_selected = df[selected_columns]

# Convert the 'close' column to strings for compatibility with DataFrameLoader
df_selected['close'] = df_selected['close'].astype(str)

# LangChain DataFrameLoader expects Pandas, no conversion needed
loader = DataFrameLoader(df_selected, page_content_column='close')
docs = loader.load()

# Initialize Ollama embeddings and LLM
embeddings = OllamaEmbeddings(model='nomic-embed-text')
llm = OllamaLLM(model='gemma3:12b')  # Updated to use langchain-ollama package

# Create Chroma vector database from documents
db = Chroma.from_documents(docs, embeddings)

# Create RAG chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Query example
query = "What was the highest closing price in the dataset?"
response = rag_chain.invoke(query)

# Output answer and source references
print("Answer:", response['result'])
for idx, doc in enumerate(response['source_documents']):
    print(f"\nSource {idx + 1}:")
    print(doc.page_content)
