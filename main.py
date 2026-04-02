from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_service import ask_llm

app = FastAPI()

# This defines the shape of data we expect to receive
class QuestionRequest(BaseModel):
    question: str
    document_name: str

@app.get("/")
def root():
    return {"message": "DocuMind is alive!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = ask_llm(
        question=request.question,
        context=""   # no document context yet - that's Phase 4
    )
    return {
        "question": request.question,
        "document": request.document_name,
        "answer": result["answer"],
        "model": result["model"],
        "tokens_used": result["tokens_used"]
    }