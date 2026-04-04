from services.pdf_service import extract_text_from_pdf, chunk_text
from services.vector_service import store_chunks, search_chunks, delete_collection
from services.llm_service import ask_llm

def process_document(file_bytes: bytes, document_id: str) -> dict:
    """
    Full pipeline: PDF bytes → text → chunks → vectors stored in DB.
    Call this when a user uploads a document.
    
    Returns info about what was processed.
    """
    # Step 1: Extract raw text from PDF
    print(f"Extracting text from PDF...")
    raw_text = extract_text_from_pdf(file_bytes)
    
    if not raw_text.strip():
        raise ValueError("Could not extract any text from this PDF.")
    
    # Step 2: Split into chunks
    print(f"Chunking text...")
    chunks = chunk_text(raw_text, chunk_size=500, overlap=50)
    
    # Step 3: Clear any existing data for this document
    delete_collection(document_id)
    
    # Step 4: Store chunks in vector database
    print(f"Storing {len(chunks)} chunks in vector DB...")
    store_chunks(document_id, chunks)
    
    return {
        "document_id": document_id,
        "total_characters": len(raw_text),
        "total_chunks": len(chunks),
        "status": "ready"
    }

def answer_question(question: str, document_id: str) -> dict:
    """
    Full RAG query: question → find relevant chunks → LLM answer.
    Call this when a user asks a question about a document.
    """
    # Step 1: Find the most relevant chunks for this question
    print(f"Searching for relevant chunks...")
    relevant_chunks = search_chunks(document_id, question, n_results=3)
    
    if not relevant_chunks:
        return {
            "answer": "No relevant content found in the document.",
            "sources": [],
            "tokens_used": 0
        }
    
    # Step 2: Join chunks into context string
    context = "\n\n---\n\n".join(relevant_chunks)
    
    # Step 3: Send question + context to LLM
    print(f"Asking LLM with {len(relevant_chunks)} chunks as context...")
    result = ask_llm(question=question, context=context)
    
    return {
        "answer": result["answer"],
        "sources": relevant_chunks,   # show user which chunks were used
        "tokens_used": result["tokens_used"]
    }