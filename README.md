# DocuMind — AI-Powered Document Q&A

> Upload any PDF and ask questions about it in plain English. DocuMind uses Retrieval-Augmented Generation (RAG) to find the most relevant sections of your document and generate accurate, source-attributed answers.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws)

## Live Demo
**[http://54.205.190.67:5173](http://54.205.190.67:5173)**

---

## What it does

1. **Upload a PDF** — drag and drop any document into the app
2. **Automatic processing** — the document is parsed, split into chunks, and stored as vector embeddings
3. **Ask questions** — type any question in plain English
4. **Get answers with sources** — the AI finds the most relevant sections and generates a grounded answer, showing exactly which parts of the document it used

---

## Architecture
┌─────────────────┐     ┌──────────────────────────────────────────────┐
│   React Frontend │────▶│              FastAPI Backend                  │
│   (Vite + JS)   │     │                                              │
└─────────────────┘     │  ┌─────────────┐      ┌──────────────────┐  │
│  │ PDF Service │      │   RAG Service    │  │
│  │             │      │                  │  │
│  │ • Parse PDF │      │ • Orchestrate    │  │
│  │ • Chunk text│      │   pipeline       │  │
│  └─────────────┘      └──────────────────┘  │
│                                              │
│  ┌─────────────┐      ┌──────────────────┐  │
│  │Vector Service│      │   LLM Service    │  │
│  │             │      │                  │  │
│  │ • ChromaDB  │      │ • OpenAI API     │  │
│  │ • Embeddings│      │ • gpt-4o-mini    │  │
│  │ • Semantic  │      │ • Source-cited   │  │
│  │   search    │      │   responses      │  │
│  └─────────────┘      └──────────────────┘  │
└──────────────────────────────────────────────┘
│
┌────────────────▼─────────────────┐
│          AWS EC2 (t2.micro)       │
│     Docker + docker-compose       │
└──────────────────────────────────┘

---

## RAG Pipeline
PDF Upload → Text Extraction → Chunking (500 chars, 50 overlap)
→ OpenAI Embeddings → ChromaDB Storage
Question → OpenAI Embedding → Semantic Search (top 3 chunks)
→ GPT-4o-mini with context → Answer + Sources

---

## Tech Stack


| Frontend | React 18, Vite |
| Backend  | Python, FastAPI |
| AI / LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector DB | ChromaDB |
| PDF Parsing | PyPDF2 |
| Deployment | Docker, AWS EC2 |
| CI/CD | GitHub Actions |

---

## Project Structure
documind/
├── main.py                 # FastAPI app and routes
├── services/
│   ├── rag_service.py      # RAG orchestration pipeline
│   ├── llm_service.py      # OpenAI LLM integration
│   ├── vector_service.py   # ChromaDB vector store
│   └── pdf_service.py      # PDF parsing and chunking
├── frontend/
│   └── src/
│       └── App.jsx         # React chat interface
├── Dockerfile              # Backend container
├── docker-compose.yml      # Multi-service orchestration
└── requirements.txt        # Python dependencies

---

## Running Locally

**Prerequisites:** Python 3.11+, Node.js 20+, OpenAI API key

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/documind.git
cd documind

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your OpenAI key
echo "OPENAI_API_KEY=your-key-here" > .env

# Start backend
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

---

## Running with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/upload` | Upload and process a PDF |
| POST | `/ask` | Ask a question about a document |

---

## Key Engineering Decisions

**Why RAG over fine-tuning?** RAG allows the model to answer questions about any document without retraining. It's cheaper, faster to deploy, and produces source-attributed answers.

**Why ChromaDB?** It runs locally with no external service required, making it simple to develop and containerize.

**Why chunk with overlap?** A 50-character overlap between chunks prevents answers from being split across chunk boundaries.

**Why OpenAI embeddings over local models?** The original implementation used `sentence-transformers` locally, but switched to OpenAI's `text-embedding-3-small` for production to reduce Docker image size from ~3GB to ~500MB.

---

## Author

Built by Bharath Bhaskar
