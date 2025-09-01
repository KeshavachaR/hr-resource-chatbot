---
title: HR Resource Chatbot
emoji: 🧑‍💼
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🧑‍💼 HR Resource Chatbot

An AI-powered chatbot designed to query structured HR datasets efficiently using semantic search and natural language generation. Built with a modular architecture featuring a FastAPI backend, Streamlit frontend, and local LLM support (Ollama + Llama3).

---

## 🚀 Features

- 🔍 **Hybrid Retrieval**: FAISS-based semantic search with optional lexical fallback.
- 🤖 **Local LLM Integration**: Uses Llama3 (via Ollama) for context-aware, natural language responses.
- ⚡ **FastAPI Backend**: Clean REST API for chat and health endpoints.
- 🎨 **Streamlit Frontend**: Interactive and user-friendly chat interface.
- 🛠️ **Resilient Design**: Graceful fallback to semantic-only mode if LLM is unavailable.
- 🖥️ **Flexible Deployment**: Run locally, in Docker, or on Hugging Face Spaces (GPU/CPU).

---

## 🧱 Architecture

**Core Components:**

- **Data Layer** → `employees.json` structured HR dataset.
- **Retriever** → SentenceTransformers + FAISS for embedding-based semantic search.
- **Generator** → Local LLM (Llama3 via Ollama) for answer synthesis.
- **API Layer** → FastAPI app with `/chat` and `/health` endpoints.
- **UI Layer** → Streamlit-based frontend for user interaction.

**Deployment Modes:**

| Mode        | Description                                  |
|-------------|----------------------------------------------|
| 🟢 GPU      | Full chatbot with Ollama + Llama3            |
| 🔵 CPU      | Fallback chatbot (semantic search only)      |
| ⚪ ZeroGPU  | Limited CPU-only demo (LLM not available)     |

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
git clone https://huggingface.co/spaces/keshav1236/hr-resource-chatbot

cd hr-resource-chatbot

### 2.Install Dependencies
pip install -r requirements.txt

### 3.Run Backend(FastAPI)
uvicorn app.main:app --reload --port 8000

### 4.Run Frontend
streamlit run frontend/streamlit_app.py

🧪 API Documentation
✅ GET /health

Health check endpoint.

Response:

{
  "status": "ok",
  "mode": "semantic",
  "semantic_available": true
}

💬 POST /chat

Submit an HR query.

Request:

{
  "query": "Find Python developers in Bengaluru"
}


Response:

{
  "answer": "Found 2 Python developers with 3+ years experience in Bengaluru."
}

📁 Example HR Dataset Structure (employees.json)
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "title": "Senior Python Developer",
    "skills": [
      "Python",
      "Django",
      "AWS",
      "Docker"
    ],
    "experience_years": 6,
    "projects": [
      "E-commerce Platform",
      "Healthcare Dashboard",
      "Data Pipeline on AWS"
    ],
    "availability": "available",
    "domains": [
      "ecommerce",
      "healthcare"
    ],
    "location": "Bengaluru"
  },
  {
    "id": 2,
    "name": "Michael Rodriguez",
    "title": "ML Engineer",
    "skills": [
      "Machine Learning",
      "scikit-learn",
      "pandas",
      "AWS"
    ],
    "experience_years": 4,
    "projects": [
      "Patient Risk Prediction System",
      "Fraud Detection"
    ],
    "availability": "available",
    "domains": [
      "healthcare",
      "fintech"
    ],
    "location": "Hyderabad"
  }
]


📌 Technical Stack

LLM Serving → Ollama
 with LLaMA3

Semantic Search → FAISS + SentenceTransformers

Backend API → FastAPI

Frontend UI → Streamlit

Containerization → Docker (GPU + CPU Dockerfiles)

Deployment → Hugging Face Spaces (ZeroGPU, CPU, or GPU modes)

💡 Future Enhancements

🔐 Add authentication for secure query access.

📂 Support uploading custom HR datasets.

📊 Add filters and visual HR analytics to the UI.

⚙️ Optimize Ollama LLM serving for faster responses.

🧠 Example Queries

"List Java developers with 5+ years of experience."

"Who are the data scientists in New York?"

"Find remote HR managers in Bengaluru."

📦 Docker Support

The Hugging Face Space uses the provided Dockerfile (for GPU).
For CPU-only environments, use Dockerfile.cpu in Settings → Dockerfile path.

🤝 Contributing

PRs and feedback are welcome! Please open an issue for feature requests or bugs.
