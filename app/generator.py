import os
import requests
from typing import List, Dict, Any

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

SYSTEM_PROMPT = '''You are an HR assistant that recommends suitable employees based on a user query.
Be precise, concise, and justify each recommendation with skills, years, and relevant projects.
If data is missing, state assumptions. Keep the tone professional.'''

def build_prompt(user_query: str, profiles: List[Dict[str, Any]]) -> str:
    lines = []
    lines.append(f"User query: {user_query}\n")
    lines.append("Candidate shortlist:\n")
    for i, emp in enumerate(profiles, 1):
        lines.append(f"{i}. {emp['name']} — {emp['title']} ({emp['experience_years']} yrs) | Skills: {', '.join(emp['skills'])} | Projects: {', '.join(emp['projects'])} | Domains: {', '.join(emp['domains'])} | Location: {emp['location']} | Availability: {emp['availability']}")
    lines.append("\nWrite a brief, structured recommendation focusing on best-fit reasoning.")
    return "\n".join(lines)

def template_answer(user_query: str, profiles: List[Dict[str, Any]]) -> str:
    if not profiles:
        return "I couldn't find strong matches. Try adding skills, years of experience, domain or location."
    lines = [f"Based on your query, here are {len(profiles)} recommended profiles:"]
    for emp in profiles:
        lines.append(f"- {emp['name']} ({emp['title']}, {emp['experience_years']} yrs) — Skills: {', '.join(emp['skills'])}; Projects: {', '.join(emp['projects'])}; Availability: {emp['availability']}")
    lines.append("Would you like me to verify availability or share contact details?")
    return "\n".join(lines)

def generate_with_ollama(user_query: str, profiles: List[Dict[str, Any]]) -> str:
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": build_prompt(user_query, profiles),
            "system": SYSTEM_PROMPT,
            "stream": False
        }
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            txt = data.get("response") or data.get("output") or ""
            if txt.strip():
                return txt.strip()
        return template_answer(user_query, profiles)
    except Exception:
        return template_answer(user_query, profiles)