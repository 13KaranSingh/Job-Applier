from pydantic import BaseModel


class RankingBreakdown(BaseModel):
    total_score: float
    recency: float
    title_fit: float
    seniority_fit: float
    company_priority: float
    prestige: float
    compensation: float
    location_fit: float
    skills_fit: float
    role_family_fit: float
    source_quality: float
    automation_readiness: float
    friction_penalty: float
    exclusion_penalty: float
    swe_score: float
    quant_score: float
    interview_probability: float
    explanations: list[str]

