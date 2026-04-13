def reason_if(score: float, threshold: float, positive: str) -> list[str]:
    return [positive] if score >= threshold else []

