from app.search import retrieve
from app.data import load_employees

def test_simple_python():
    employees = load_employees()
    q = "Find Python developers with 3+ years experience"
    results = retrieve(q, employees, top_k=5)
    assert len(results) >= 1
    assert "python" in [s.lower() for s in results[0][0]["skills"]]