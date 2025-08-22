from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    id: int
    name: str
    title: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
    domains: List[str]
    location: str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    recommendations: List[Employee]

class SearchQuery(BaseModel):
    skills: Optional[List[str]] = None
    min_experience: Optional[int] = None
    project: Optional[str] = None
    availability: Optional[str] = None
    domain: Optional[str] = None
    location: Optional[str] = None