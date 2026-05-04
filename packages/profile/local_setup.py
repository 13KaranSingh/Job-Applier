import json
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.profile import AnswerLibrary, CandidateProfile, ResumeAsset

DEFAULT_ANSWER_LIBRARY = [
    {
        "answer_key": "work_authorized_us",
        "category": "work_authorization",
        "prompt_patterns": ["authorized to work", "work authorization", "legally authorized"],
        "answer_text": "Yes, I am a U.S. citizen and authorized to work in the United States.",
        "requires_human_review": False,
    },
    {
        "answer_key": "need_sponsorship",
        "category": "work_authorization",
        "prompt_patterns": ["sponsorship", "visa sponsorship", "require sponsorship"],
        "answer_text": "No, I do not require visa sponsorship.",
        "requires_human_review": False,
    },
    {
        "answer_key": "relocate_yes",
        "category": "location",
        "prompt_patterns": ["willing to relocate", "relocation"],
        "answer_text": "Yes, I am willing to relocate for the right opportunity.",
        "requires_human_review": False,
    },
    {
        "answer_key": "salary_expectation_general",
        "category": "compensation",
        "prompt_patterns": ["salary expectation", "desired salary", "compensation expectation"],
        "answer_text": "My target base salary is at least $140,000, but I am flexible based on total compensation, role scope, location, and growth opportunity.",
        "requires_human_review": True,
    },
    {
        "answer_key": "years_python",
        "category": "skills",
        "prompt_patterns": ["years of python", "python experience"],
        "answer_text": "4-5 years",
        "requires_human_review": False,
    },
    {
        "answer_key": "years_typescript",
        "category": "skills",
        "prompt_patterns": ["years of typescript", "typescript experience"],
        "answer_text": "4-5 years",
        "requires_human_review": False,
    },
    {
        "answer_key": "years_react",
        "category": "skills",
        "prompt_patterns": ["years of react", "react experience"],
        "answer_text": "4-5 years",
        "requires_human_review": False,
    },
    {
        "answer_key": "years_cpp",
        "category": "skills",
        "prompt_patterns": ["years of c++", "c++ experience", "cpp experience"],
        "answer_text": "4-5 years",
        "requires_human_review": False,
    },
]


def load_local_profile(path: str = "config/local/profile.json") -> dict[str, Any]:
    return json.loads(Path(path).read_text())


def seed_local_profile(session: Session, path: str = "config/local/profile.json") -> dict[str, int]:
    payload = load_local_profile(path)
    profile = session.scalars(select(CandidateProfile).limit(1)).first()
    if profile is None:
        profile = CandidateProfile(profile_json=payload["profile"])
    else:
        profile.profile_json = payload["profile"]
    session.add(profile)

    resumes_seeded = 0
    for resume in payload.get("resume_assets", []):
        existing_resume = session.scalars(
            select(ResumeAsset).where(ResumeAsset.variant_name == resume["variant_name"])
        ).first()
        if existing_resume is None:
            existing_resume = ResumeAsset(
                variant_name=resume["variant_name"],
                file_path=resume["file_path"],
                active=resume.get("active", True),
                metadata_json=resume.get("metadata_json", {}),
            )
            resumes_seeded += 1
        else:
            existing_resume.file_path = resume["file_path"]
            existing_resume.active = resume.get("active", existing_resume.active)
            existing_resume.metadata_json = resume.get("metadata_json", existing_resume.metadata_json)
        session.add(existing_resume)

    answers_seeded = 0
    for answer in DEFAULT_ANSWER_LIBRARY:
        existing_answer = session.scalars(
            select(AnswerLibrary).where(AnswerLibrary.answer_key == answer["answer_key"])
        ).first()
        if existing_answer is None:
            existing_answer = AnswerLibrary(
                answer_key=answer["answer_key"],
                category=answer["category"],
                prompt_patterns_json=answer["prompt_patterns"],
                answer_text=answer["answer_text"],
                requires_human_review=answer["requires_human_review"],
                active=True,
            )
            answers_seeded += 1
        else:
            existing_answer.category = answer["category"]
            existing_answer.prompt_patterns_json = answer["prompt_patterns"]
            existing_answer.answer_text = answer["answer_text"]
            existing_answer.requires_human_review = answer["requires_human_review"]
            existing_answer.active = True
        session.add(existing_answer)

    session.commit()
    return {"profiles_seeded": 1, "resumes_seeded": resumes_seeded, "answers_seeded": answers_seeded}
