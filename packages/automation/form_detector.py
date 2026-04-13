def detect_form_complexity(page_text: str) -> str:
    lowered = page_text.lower()
    if "essay" in lowered or "cover letter" in lowered:
        return "high"
    if "salary expectation" in lowered:
        return "medium"
    return "low"

