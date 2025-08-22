import json
from typing import List, Dict, Any
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "employees.json"

def load_employees() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["employees"]