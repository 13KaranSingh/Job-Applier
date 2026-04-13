from collections.abc import Iterable


def match_answer(prompt: str, answers: Iterable[dict]) -> dict | None:
    normalized = prompt.lower()
    for answer in answers:
        for pattern in answer.get("prompt_patterns", []):
            if pattern.lower() in normalized:
                return answer
    return None

