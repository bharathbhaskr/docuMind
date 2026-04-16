import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

embedding_fn = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path="./chroma_db")

def get_or_create_collection(collection_name: str):
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

def store_chunks(collection_name: str, chunks: list[str]) -> int:
    collection = get_or_create_collection(collection_name)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    return len(chunks)

def search_chunks(collection_name: str, query: str, n_results: int = 3) -> list[str]:
    collection = get_or_create_collection(collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0]

def delete_collection(collection_name: str):
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass