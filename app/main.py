from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from .data import load_employees
from .search import retrieve as lexical_retrieve, generate_answer as lexical_answer
from .models import Employee, ChatRequest, ChatResponse
from .retriever import SemanticRetriever
from .generator import generate_with_ollama, template_answer

app = FastAPI(title="HR Resource Query Chatbot", version="0.2.0 (advanced)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMPLOYEES = load_employees()
RETRIEVER = SemanticRetriever(EMPLOYEES)

HR_MODE = os.getenv("HR_MODE", "semantic")  # 'semantic' or 'lexical'

@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": HR_MODE,
        "semantic_available": RETRIEVER.available
    }

@app.get("/employees/search", response_model=List[Employee])
def employees_search(
    skills: Optional[List[str]] = Query(default=None),
    min_experience: Optional[int] = Query(default=None, ge=0),
    project: Optional[str] = None,
    availability: Optional[str] = Query(default=None, regex="^(available|busy)$"),
    domain: Optional[str] = None,
    location: Optional[str] = None,
):
    results = []
    for e in EMPLOYEES:
        if skills:
            es = {s.lower() for s in e["skills"]}
            if not all(s.lower() in es for s in skills):
                continue
        if min_experience is not None and e["experience_years"] < min_experience:
            continue
        if project and project.lower() not in " ".join(e["projects"]).lower():
            continue
        if availability and e["availability"] != availability:
            continue
        if domain and domain.lower() not in [d.lower() for d in e["domains"]]:
            continue
        if location and location.lower() != e["location"].lower():
            continue
        results.append(e)
    return results

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    query = (req.query or "").strip()
    if len(query) < 3:
        raise HTTPException(status_code=400, detail="Query too short")

    use_semantic = (HR_MODE == "semantic") and RETRIEVER.available
    if use_semantic:
        pairs = RETRIEVER.search(query, top_k=5)
        recs = [p[0] for p in pairs]
        answer = generate_with_ollama(query, recs)
        if not answer or len(answer.strip()) == 0:
            answer = template_answer(query, recs)
        return {"answer": answer, "recommendations": recs}
    else:
        pairs = lexical_retrieve(query, EMPLOYEES, top_k=5)
        recs = [p[0] for p in pairs]
        answer = lexical_answer(query, pairs)
        return {"answer": answer, "recommendations": recs}