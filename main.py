from fastapi import FastAPI

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
    # For now we return a fake answer - the real AI comes in Phase 4!
    return {
        "question": request.question,
        "document": request.document_name,
        "answer": "AI answer coming soon...",
        "status": "ok"
    }