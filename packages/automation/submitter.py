def confirm_submission(page_text: str) -> bool:
    lowered = page_text.lower()
    return "application submitted" in lowered or "thank you for applying" in lowered

