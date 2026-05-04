from dataclasses import dataclass
from typing import Any

from packages.adapters.parsing.normalization import classify_experience_level, classify_role_family
from packages.core.constants import NEGATIVE_KEYWORDS
from packages.core.enums import DecisionClass, OperatingMode
from packages.ranking.explanations import reason_if
from packages.ranking.feature_extractors import role_family_fit, skill_overlap_score
from packages.ranking.formulas import bounded, score_recency
from packages.schemas.job import JobSchema, JobScoreSchema
from packages.schemas.profile import CandidateProfileSchema


@dataclass(slots=True)
class CompanyMetadata:
    target_priority: int = 0
    prestige_tier: int = 1
    compensation_tier: int = 1
    role_bias: str = "both"
    blacklisted: bool = False


def _score_title_fit(title: str) -> float:
    normalized = title.lower()
    strong = [
        "software engineer",
        "sde",
        "frontend engineer",
        "full stack engineer",
        "quantitative trader",
        "quantitative researcher",
        "quantitative developer",
    ]
    moderate = ["platform engineer", "research engineer", "trading systems engineer", "backend engineer"]
    if any(item in normalized for item in strong):
        return 11.0
    if any(item in normalized for item in moderate):
        return 8.0
    return 2.0


def _score_seniority(level: str) -> float:
    mapping = {"new_grad": 10.0, "entry": 8.0, "associate": 7.0, "mid": 5.0, "senior": 0.0, "unknown": 4.0}
    return mapping.get(level, 0.0)


def _score_company_priority(metadata: CompanyMetadata) -> float:
    return round((metadata.target_priority / 100) * 10, 2)


def _score_prestige(metadata: CompanyMetadata) -> float:
    return {5: 8.0, 4: 6.0, 3: 4.0, 2: 2.0, 1: 1.0}.get(metadata.prestige_tier, 1.0)


def _score_compensation(metadata: CompanyMetadata, salary_max: float | None) -> float:
    if salary_max:
        if salary_max >= 250000:
            return 8.0
        if salary_max >= 180000:
            return 6.0
        if salary_max >= 120000:
            return 4.0
        return 2.0
    return {5: 7.0, 4: 5.0, 3: 3.0, 2: 2.0, 1: 1.0}.get(metadata.compensation_tier, 1.0)


def _score_location(location: str | None, preferred_locations: list[str], remote_policy: str) -> float:
    if remote_policy == "remote":
        return 7.0
    if location and location in preferred_locations:
        return 6.0
    if location and any(token in location.lower() for token in ["new york", "san francisco", "bay area"]):
        return 5.0
    return 2.0


def _source_quality(source_name: str) -> float:
    lowered = source_name.lower()
    if any(item in lowered for item in ["greenhouse", "lever", "google", "amazon", "jane street", "citadel"]):
        return 4.0
    return 2.0


def _automation_readiness(auto_apply_supported: bool, parser_confidence: float, automation_confidence: float) -> float:
    if auto_apply_supported and parser_confidence >= 0.8 and automation_confidence >= 0.8:
        return 6.0
    if parser_confidence >= 0.6 and automation_confidence >= 0.6:
        return 3.0
    return 0.0


def _friction_penalty(description: str, auto_apply_supported: bool) -> float:
    lowered = description.lower()
    penalty = 0.0
    if "cover letter" in lowered or "essay" in lowered:
        penalty -= 3.0
    if not auto_apply_supported:
        penalty -= 2.0
    return penalty


def _exclusion_penalty(job: JobSchema) -> float:
    text = f"{job.title_normalized} {job.description_text}".lower()
    if any(keyword in text for keyword in NEGATIVE_KEYWORDS):
        return -12.0
    if job.role_family == "other":
        return -10.0
    return 0.0


def _interview_probability(title_fit: float, seniority_fit: float, skills_fit: float, role_fit: float) -> float:
    raw = (title_fit / 12) * 0.30 + (seniority_fit / 10) * 0.25 + (skills_fit / 12) * 0.25 + (role_fit / 8) * 0.20
    return round(min(1.0, raw), 4)


def select_resume_variant(role_family: str, description_text: str) -> str:
    description = description_text.lower()
    if "frontend" in description or "react" in description or "typescript" in description:
        return "resume_frontend.pdf"
    if role_family == "quant":
        if any(token in description for token in ["research", "probability", "statistics", "signal"]):
            return "resume_quant_research.pdf"
        return "resume_quant_swe.pdf"
    return "resume_swe_general.pdf"


def recommended_action(total_score: float, parser_confidence: float, automation_confidence: float, exclusion_penalty: float, friction_penalty: float, duplicate: bool = False, blacklisted: bool = False) -> str:
    if blacklisted or duplicate or exclusion_penalty <= -10:
        return DecisionClass.IGNORE.value
    if (
        total_score >= 85
        and automation_confidence >= 0.8
        and parser_confidence >= 0.8
        and exclusion_penalty == 0
        and friction_penalty > -4
    ):
        return DecisionClass.AUTO_APPLY_NOW.value
    if 70 <= total_score < 85 or automation_confidence >= 0.6 or parser_confidence >= 0.6:
        return DecisionClass.QUEUE_FOR_REVIEW.value
    if total_score >= 55:
        return DecisionClass.ALERT_ONLY.value
    return DecisionClass.IGNORE.value


def score_job(
    job: JobSchema,
    profile: CandidateProfileSchema,
    company_metadata: CompanyMetadata,
    *,
    operating_mode: OperatingMode = OperatingMode.BALANCED,
) -> JobScoreSchema:
    role_family = job.role_family or classify_role_family(job.title_normalized, job.description_text)
    experience_level = job.experience_level or classify_experience_level(job.title_normalized, job.description_text)
    recency = score_recency(job.posted_at_source)
    title_fit = _score_title_fit(job.title_normalized)
    seniority_fit = _score_seniority(experience_level)
    company_priority = _score_company_priority(company_metadata)
    prestige = _score_prestige(company_metadata)
    compensation = _score_compensation(company_metadata, job.base_salary_max_usd)
    location_fit = _score_location(job.location_normalized, profile.preferred_locations, job.remote_policy)
    skills_fit = skill_overlap_score(
        job.description_text,
        profile.skill_inventory + ["react", "typescript", "python", "c++", "java", "javascript"],
    )
    family_fit = role_family_fit(role_family, profile.target_modes)
    source_quality = _source_quality(job.company_name)
    automation = _automation_readiness(
        job.auto_apply_supported, job.parser_confidence, job.automation_confidence
    )
    friction = _friction_penalty(job.description_text, job.auto_apply_supported)
    exclusion = _exclusion_penalty(job)
    interview_prob = _interview_probability(title_fit, seniority_fit, skills_fit, family_fit)
    base_total = (
        recency
        + title_fit
        + seniority_fit
        + company_priority
        + prestige
        + compensation
        + location_fit
        + skills_fit
        + family_fit
        + source_quality
        + automation
        + friction
        + exclusion
    )
    swe_score = (
        0.25 * compensation
        + 0.20 * prestige
        + 0.15 * family_fit
        + 0.12 * skills_fit
        + 0.10 * company_priority
        + 0.08 * recency
        + 0.05 * location_fit
        + 0.05 * automation
    ) * 10
    quant_score = (
        0.30 * compensation
        + 0.22 * prestige
        + 0.15 * skills_fit
        + 0.12 * family_fit
        + 0.10 * company_priority
        + 0.06 * recency
        + 0.03 * location_fit
        + 0.02 * automation
    ) * 10
    weighted_total = base_total
    if operating_mode == OperatingMode.SWE_PRIORITY:
        weighted_total = swe_score
    elif operating_mode == OperatingMode.QUANT_PRIORITY:
        weighted_total = quant_score
    else:
        weighted_total = (swe_score + quant_score) / 2
    final_total = bounded(weighted_total + (interview_prob * 5), 0.0, 100.0)
    explanations = [
        *reason_if(recency, 9, "Fresh posting"),
        *reason_if(title_fit, 8, "Strong title fit"),
        *reason_if(prestige, 6, "High-prestige company"),
        *reason_if(compensation, 5, "Strong compensation signal"),
        *reason_if(family_fit, 6, "Good role-family alignment"),
    ]
    action = recommended_action(
        final_total,
        job.parser_confidence,
        job.automation_confidence,
        exclusion,
        friction,
        blacklisted=company_metadata.blacklisted,
    )
    return JobScoreSchema(
        job_id=str(job.id or job.canonical_job_key),
        total_score=round(final_total, 2),
        recency_score=recency,
        title_fit_score=title_fit,
        seniority_fit_score=seniority_fit,
        company_priority_score=company_priority,
        prestige_score=prestige,
        compensation_score=compensation,
        location_fit_score=location_fit,
        skills_fit_score=skills_fit,
        role_family_fit_score=family_fit,
        source_quality_score=source_quality,
        automation_readiness_score=automation,
        friction_penalty=friction,
        exclusion_penalty=exclusion,
        recommended_resume_variant=select_resume_variant(role_family, job.description_text),
        recommended_action=action,
        explanations=explanations,
        swe_score=round(swe_score, 2),
        quant_score=round(quant_score, 2),
        interview_probability=interview_prob,
    )
