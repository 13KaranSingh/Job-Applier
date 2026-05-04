from pydantic import BaseModel, Field


class CandidateProfileSchema(BaseModel):
    full_name: str
    email: str = "karanvir_gurn@yahoo.com"
    phone: str
    current_city: str
    current_state: str
    country: str = "USA"
    github_url: str
    portfolio_url: str
    school_name: str
    degree: str
    major: str
    graduation_month: str
    graduation_year: int = 2026
    work_authorization: str = "authorized"
    sponsorship_needed: bool = False
    willing_to_relocate: bool = True
    preferred_locations: list[str] = Field(
        default_factory=lambda: ["San Francisco Bay Area", "New York City", "Remote"]
    )
    target_modes: list[str] = Field(default_factory=lambda: ["swe", "quant"])
    target_companies: list[str] = Field(default_factory=list)
    excluded_companies: list[str] = Field(default_factory=list)
    skill_inventory: list[str] = Field(default_factory=list)
    years_experience_total: float | None = None
    minimum_base_salary_usd: int | None = None
    experience_band: str = "new_grad_to_mid"
    resume_variants: list[str] = Field(
        default_factory=lambda: [
            "resume_swe_general.pdf",
            "resume_frontend.pdf",
            "resume_quant_swe.pdf",
        ]
    )


class AnswerLibrarySchema(BaseModel):
    answer_key: str
    category: str
    prompt_patterns: list[str]
    answer_text: str
    requires_human_review: bool = False
    active: bool = True
