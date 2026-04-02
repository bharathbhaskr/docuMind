import chromadb
from chromadb.utils import embedding_functions

# Use a free local embedding model - no API key needed
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# This creates a local database folder called "chroma_db" in your project
client = chromadb.PersistentClient(path="./chroma_db")

def get_or_create_collection(collection_name: str):
    """
    Get an existing collection or create a new one.
    Think of a collection like a table in a regular database.
    Each document you upload will get its own collection.
    """
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

def store_chunks(collection_name: str, chunks: list[str]) -> int:
    """
    Store a list of text chunks into the vector database.
    Each chunk gets embedded (converted to numbers) automatically.

    chunks:  a list of text strings e.g. ["Paris is...", "France has..."]
    returns: how many chunks were stored
    """
    collection = get_or_create_collection(collection_name)

    # ChromaDB needs a unique ID for each chunk
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,   # the actual text
        ids=ids             # unique identifiers
    )

    return len(chunks)

def search_chunks(collection_name: str, query: str, n_results: int = 3) -> list[str]:
    """
    Search for the most relevant chunks for a given query.
    Returns the top n_results most semantically similar chunks.
    """
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_texts=[query],    # ChromaDB embeds this automatically
        n_results=n_results
    )

    # results["documents"] is a list of lists - we want the inner list
    return results["documents"][0]

def delete_collection(collection_name: str):
    """
    Delete all stored chunks for a document.
    Useful when a user re-uploads a document.
    """
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass  # collection didn't exist, that's fine