import re
from typing import List, Dict, Any, Tuple
from collections import Counter
import math

def normalize(text: str) -> List[str]:
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\+\-\.]*", text)
    return tokens

ALIASES = {
    "ml": ["machine", "learning", "ml"],
    "machinelearning": ["machine", "learning", "ml"],
    "ai": ["ai", "artificial", "intelligence"],
    "reactnative": ["react", "native", "react-native"],
    "cv": ["computer", "vision", "cv"],
    "nlp": ["nlp", "natural", "language", "processing"],
    "k8s": ["kubernetes", "k8s"],
    "devops": ["devops", "sre", "platform"],
    "aws": ["aws", "amazon", "web", "services"],
    "gcp": ["gcp", "google", "cloud"],
    "azure": ["azure"],
    "db": ["database", "sql", "postgres", "mysql"],
}

def expand_aliases(tokens: List[str]) -> List[str]:
    expanded = list(tokens)
    joined = "".join(tokens)
    for key, words in ALIASES.items():
        if key in joined or any(w in tokens for w in words):
            expanded.extend(words + [key])
    return expanded

def bow(text: str) -> Counter:
    tokens = normalize(text)
    tokens = expand_aliases(tokens)
    return Counter(tokens)

def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[t] * b.get(t, 0) for t in a)
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def make_profile_text(emp: Dict[str, Any]) -> str:
    parts = [
        emp.get("name",""),
        emp.get("title",""),
        " ".join(emp.get("skills", [])),
        " ".join(emp.get("projects", [])),
        " ".join(emp.get("domains", [])),
        emp.get("location",""),
        emp.get("availability",""),
        f"{emp.get('experience_years',0)} years"
    ]
    return " ".join(parts)

def parse_query(query: str) -> Dict[str, Any]:
    q = query.lower()
    want = {
        "min_experience": None,
        "availability": None,
        "skills": [],
        "domain": None,
        "project_keywords": [],
        "location": None
    }
    m = re.search(r"(\d+)\s*\+?\s*year", q)
    if m:
        want["min_experience"] = int(m.group(1))
    if "available" in q or "immediately" in q:
        want["availability"] = "available"
    tokens = normalize(q)
    known_skills = {"python","django","aws","docker","react","reactnative","react-native","typescript","node.js","node","gcp","azure",
                    "pytorch","tensorflow","computer","vision","ml","machine","learning","nlp","transformers","spark","airflow",
                    "fastapi","sql","powerbi","kubernetes","terraform","mongodb","redis","postgre","postgresql","spacy","vector","db"}
    for t in tokens:
        clean = t.replace(".", "").replace("-", "")
        if clean in known_skills:
            want["skills"].append(t)
    for dom in ["healthcare","health","fintech","ecommerce","saas","retail","legal","legaltech","hr","hrtech","iot","logistics","adtech","telecom","enterprise"]:
        if dom in q:
            want["domain"] = "healthcare" if dom in ["healthcare","health"] else ("legaltech" if dom in ["legal","legaltech"] else ("hrtech" if dom in ["hr","hrtech"] else dom))
    pk = re.findall(r"(?:project|projects|worked on) ([a-zA-Z\s\-]+)", q)
    if pk:
        want["project_keywords"] = [p.strip() for p in pk]
    for loc in ["bengaluru","bangalore","mumbai","pune","delhi","noida","hyderabad","chennai","ahmedabad","gurugram","remote"]:
        if loc in q:
            want["location"] = "Bengaluru" if loc in ["bengaluru","bangalore"] else loc.title()
    return want

def score_employee(emp: Dict[str, Any], query: str, want: Dict[str, Any]) -> float:
    text = make_profile_text(emp)
    s = 0.0
    s += 0.6 * cosine(bow(query), bow(text))
    if want.get("min_experience") is not None:
        s += 0.15 if emp.get("experience_years", 0) >= want["min_experience"] else -0.2
    if want.get("availability") == "available":
        s += 0.1 if emp.get("availability") == "available" else -0.1
    skills = set([k.replace('.', '').replace('-', '') for k in want.get("skills", [])])
    emp_skills = set([k.lower().replace('.', '').replace('-', '') for k in emp.get("skills", [])])
    if skills:
        inter = skills & emp_skills
        s += 0.25 * (len(inter) / max(1, len(skills)))
    want_dom = want.get("domain")
    if want_dom:
        s += 0.1 if want_dom in [d.lower() for d in emp.get("domains", [])] else 0.0
    for kw in want.get("project_keywords", []):
        if kw.lower() in " ".join(emp.get("projects", [])).lower():
            s += 0.05
    want_loc = want.get("location")
    if want_loc:
        if want_loc.lower() == "remote" and emp.get("location","").lower() == "remote":
            s += 0.05
        elif want_loc.lower() == emp.get("location","").lower():
            s += 0.05
    return s

def retrieve(query: str, employees: List[Dict[str, Any]], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
    want = parse_query(query)
    scored = [(emp, score_employee(emp, query, want)) for emp in employees]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = [(e,s) for e,s in scored[: top_k*2] if s > 0.05][:top_k]
    return results

def generate_answer(query: str, results: List[Tuple[Dict[str, Any], float]]) -> str:
    if not results:
        return "I couldn't find a strong match. Try adding skills, years of experience, or domain keywords."
    lines = [f"Based on your query, here are {len(results)} recommended profiles:"]
    for emp, score in results:
        lines.append(f"- **{emp['name']}** ({emp['title']}, {emp['experience_years']} yrs) — Skills: {', '.join(emp['skills'])}; Projects: {', '.join(emp['projects'])}; Availability: {emp['availability']}")
    lines.append("Would you like me to check their current availability or share contact details?")
    return "\n".join(lines)