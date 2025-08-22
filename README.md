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

The HR Resource Query Chatbot is an AI-powered assistant that helps HR teams quickly find employees based on natural language queries. It uses a Retrieval-Augmented Generation (RAG) pipeline to match employee profiles with HR queries and generate context-rich recommendations.

Example queries:

"Find Python developers with 3+ years of experience"

"Who has worked on healthcare projects?"

"Suggest people for a React Native project"

This solution supports offline execution with local LLMs via Ollama, semantic search using FAISS, and a user-friendly Streamlit interface.

Features

✔ Natural Language HR Queries
✔ Semantic Search with FAISS and Sentence-Transformers
✔ Local LLM (Llama3) Integration via Ollama
✔ Hybrid Retrieval (Semantic + Lexical Fallback)
✔ Caching for Fast Startup (FAISS Index Reuse)
✔ FastAPI Backend with REST APIs
✔ Streamlit Frontend for Chat & Filtered Search
✔ Offline Mode (No external APIs required)

Architecture
flowchart LR
    A[User] --> B[Streamlit UI]
    B --> C[FastAPI Backend]
    C --> D[RAG Engine]
    D --> E[FAISS + Embeddings]
    D --> F[Ollama LLM]
    D --> G[Employee Dataset (JSON)]

Architecture Diagram

Screenshots

(Replace placeholders with actual screenshots)

Chat Interface

Employee Results

Setup & Installation
Prerequisites

Python 3.9+

Ollama installed locally (Download Ollama
)

Models pulled:

ollama pull llama3

1. Clone the Repository
git clone https://github.com/KeshavachaR/hr-resource-chatbot.git
cd hr-resource-chatbot

2. Create Virtual Environment & Install Dependencies
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install --upgrade pip
pip install -r requirements.txt

3. Start Ollama Service

In a separate terminal:

ollama serve


Optional warm-up:

ollama run llama3 "hello"

4. Start Backend (FastAPI)
set HR_MODE=semantic
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


First run:

Builds FAISS cache in store/.

Subsequent runs will load cache for faster startup.

5. Start Frontend (Streamlit)
streamlit run frontend/streamlit_app.py --server.address 0.0.0.0 --server.port 8501


Access UI at:
http://localhost:8501

API Documentation
Endpoints
1. Health Check
GET /health
Response: { "status": "ok" }

2. Employee Search
GET /employees/search?skills=Python,AWS&min_exp=3&availability=available


Response:

{
  "results": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "skills": ["Python", "React", "AWS"],
      "experience_years": 5,
      "projects": ["E-commerce Platform", "Healthcare Dashboard"],
      "availability": "available"
    }
  ]
}

3. Chat Query
POST /chat
Body:
{
  "query": "Find Python developers with 3+ years experience",
  "top_k": 5
}


Response:

{
  "answer": "Based on your requirements, I found...",
  "candidates": [ ... ]
}

AI Development Process

Tools Used:

ChatGPT for architecture planning and code generation.

GitHub Copilot for inline coding assistance.

How AI Helped:

Generated boilerplate code for FastAPI, Streamlit, and FAISS setup.

Suggested improvements for caching and Ollama integration.

Manual Work:

Debugging FAISS index persistence.

Streamlit UI design and integration with backend.

AI Contribution: ~60% assisted, 40% manual refinement.

Challenges:

Ollama timeout handling.

Ensuring offline capability without external APIs.

Technical Decisions

Ollama for LLM:

Chosen for privacy, offline mode, and free usage vs. OpenAI API.

Sentence-Transformers + FAISS:

Fast and accurate semantic search.

FAISS for vector similarity with caching for performance.

FastAPI + Streamlit:

Simple, clean stack for quick prototyping and local deployment.

Future Improvements

Add conversation history for multi-turn context.

Implement authentication & role-based access.

Add real-time availability updates from a live DB.

Deploy Streamlit app with backend API on a single Docker container.

Support multiple local LLM models (e.g., Mistral, Qwen).

[Live Demo](https://huggingface.co/spaces/keshav1236/hr-resource-chatbot)

Local Run: Follow steps above.
