from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from services.rag_service import process_document, answer_question

app = FastAPI(title="DocuMind", description="AI-powered document Q&A")

# This defines the shape of data we expect to receive
class QuestionRequest(BaseModel):
    question: str
    document_id: str

@app.get("/")
def root():
    return {"message": "DocuMind is alive!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF and process it for Q&A.
    The document_id returned here is what you pass to /ask.
    """
    # Validate it's a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Read the file bytes
    file_bytes = await file.read()
    
    # Use filename (without .pdf) as the document ID
    document_id = file.filename.replace(".pdf", "").replace(" ", "_").lower()
    
    # Run the full processing pipeline
    result = process_document(file_bytes, document_id)
    
    return {
        "message": "Document processed successfully",
        "document_id": document_id,
        "chunks_created": result["total_chunks"],
        "characters_processed": result["total_characters"]
    }

@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Ask a question about an uploaded document.
    Use the document_id returned from /upload.
    """
    result = answer_question(
        question=request.question,
        document_id=request.document_id
    )
    
    return {
        "question": request.question,
        "document_id": request.document_id,
        "answer": result["answer"],
        "sources_used": result["sources"],
        "tokens_used": result["tokens_used"]
    }