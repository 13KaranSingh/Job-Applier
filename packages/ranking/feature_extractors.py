from collections.abc import Iterable

from packages.adapters.parsing.normalization import classify_role_family, normalize_title


def skill_overlap_score(description_text: str, skills: Iterable[str], max_score: float = 12.0) -> float:
    description = description_text.lower()
    normalized_skills = {normalize_title(skill) for skill in skills if skill}
    matches = sum(1 for skill in normalized_skills if skill and skill in description)
    if not normalized_skills:
        return 0.0
    return min(max_score, max_score * (matches / len(normalized_skills)))


def role_family_fit(job_role_family: str, target_modes: Iterable[str]) -> float:
    targets = set(target_modes)
    if job_role_family in targets:
        return 8.0
    if job_role_family == "both":
        return 6.0
    if job_role_family == classify_role_family("research engineer") and "swe" in targets:
        return 4.0
    return 0.0

