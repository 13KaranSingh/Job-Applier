import json
import re
from typing import Any


def extract_jsonld_blocks(html: str) -> list[dict[str, Any] | list[Any]]:
    pattern = re.compile(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE)
    blocks: list[dict[str, Any]] = []
    for match in pattern.findall(html):
        try:
            parsed = json.loads(match.strip())
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict | list):
            blocks.append(parsed)
    return blocks
