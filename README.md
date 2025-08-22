---
title: HR Resource Chatbot
emoji: 🧑‍💼
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

HR Resource Query Chatbot
Overview

The HR Resource Query Chatbot is an AI-powered system designed to help HR managers quickly find suitable employees for projects. It uses a RAG (Retrieval-Augmented Generation) approach combining vector search (FAISS) with a local LLM (Ollama + llama3). The chatbot understands natural language queries like:

“Find Python developers with 3+ years of healthcare experience, available in Bengaluru.”

and returns a ranked list of matching employees with reasoning.

Features

🔎 Semantic search with HuggingFace embeddings + FAISS

📝 LLM-powered answers via local Ollama (llama3)

🛠️ Fallback lexical search (if embeddings/FAISS unavailable)

🌐 FastAPI backend with clean /chat, /employees/search, /health endpoints

💻 Streamlit frontend for conversational queries + advanced filters

💾 Persistent FAISS index auto-rebuilt only when employee dataset changes

🧩 Modular architecture (retriever, generator, search) for extensibility

⚡ Optimized response time with cached embeddings

Architecture
+------------------+        +--------------------+        +-------------------+
|   Streamlit UI   | <----> |   FastAPI Backend  | <----> |  FAISS Vector DB  |
+------------------+        +--------------------+        +-------------------+
        |                              |                          |
        |   /chat, /search APIs         |    Embeddings (SBERT)   |
        |                              |                          |
        +----------------------------------------------------------+
                          Ollama (llama3 LLM)


Components

app/search.py → Lexical retrieval + query parsing

app/retriever.py → Semantic search (embeddings + FAISS)

app/generator.py → Local LLM (Ollama llama3) answer generation

app/main.py → FastAPI endpoints

frontend/streamlit_app.py → Chat UI + advanced filters

Setup & Installation
1. Clone & Setup
git clone <repo_url>
cd hr_resource_chatbot_adv
python -m venv .venv
# Activate venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

2. Install Dependencies
pip install -r requirements.txt
pip install sentence-transformers faiss-cpu

3. Start Ollama
ollama serve
ollama pull llama3

4. Run FastAPI Backend
# Windows PowerShell
$env:HR_MODE="semantic"
$env:HR_EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
$env:OLLAMA_URL="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="llama3"

uvicorn app.main:app --reload

5. Run Streamlit Frontend
streamlit run frontend/streamlit_app.py

API Documentation
GET /health

Returns service status.

{"status":"ok","mode":"semantic","semantic_available":true}

POST /chat

Natural language HR queries.

Request:
{"query": "Find Python developers with 3+ years in healthcare"}

Response:
{
  "answer": "Alice Johnson is a strong fit ...",
  "recommendations": [ {...}, {...} ]
}

GET /employees/search

Filter employees via structured params.

/employees/search?skills=Python&min_experience=3&domain=healthcare&availability=available

AI Development Process

AI Tools Used: ChatGPT (for code scaffolding, architecture design, and debugging)

Phases Assisted:

Code generation: created initial FastAPI + Streamlit skeletons

Debugging: fixed serialization errors and parsing issues

Architecture decisions: advised semantic vs lexical fallback, Ollama integration

Code Breakdown:

~70% AI-assisted (initial drafts, helpers, embeddings integration)

~30% hand-written (refinements, bug fixes, environment configs)

AI Innovations:

Hybrid RAG (semantic first, lexical fallback)

Cached FAISS embeddings keyed by dataset hash

Challenges Solved Manually:

Windows-specific env variable handling

Streamlit session error debugging

Technical Decisions

Local LLM (Ollama + llama3)

✔ Privacy: no data leaves machine

✔ Cost: zero API fees

✔ Control: offline + configurable models

✘ Heavier local setup compared to cloud APIs

FAISS + SBERT embeddings

✔ Fast, scalable similarity search

✔ Works offline

✘ Requires extra installation (faiss-cpu)

Fallback lexical retrieval

✔ Ensures chatbot works even if FAISS/LLM unavailable

✔ Improves robustness for edge cases

Future Improvements

🔹 Add cross-encoder reranker for better precision

🔹 Multi-turn conversation memory (track context across queries)

🔹 Docker + docker-compose for one-click deployment

🔹 Support hybrid search (BM25 + semantic embeddings)

🔹 Integration with company HRIS/ATS APIs

Demo

Run locally with Streamlit (http://localhost:8501)

Example query:

“Find React Native developers with 2+ years, available remotely in foodtech.”
