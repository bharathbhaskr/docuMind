from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.rag_service import process_document, answer_question

app = FastAPI(title="DocuMind", description="AI-powered document Q&A")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    document_id: str

@app.get("/")
def root():
    return {"message": "DocuMind is alive!", "version": "4.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    file_bytes = await file.read()
    document_id = file.filename.replace(".pdf", "").replace(" ", "_").lower()
    result = process_document(file_bytes, document_id)
    return {
        "message": "Document processed successfully",
        "document_id": document_id,
        "chunks_created": result["total_chunks"],
        "characters_processed": result["total_characters"]
    }

@app.post("/ask")
def ask(request: QuestionRequest):
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