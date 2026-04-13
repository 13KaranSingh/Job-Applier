import json
from pathlib import Path
from typing import Any


def load_default_companies() -> list[dict[str, Any]]:
    seed_path = Path(__file__).with_name("default_companies.json")
    return json.loads(seed_path.read_text())

