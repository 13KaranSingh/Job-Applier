from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.db.models.profile import AnswerLibrary, CandidateProfile, ResumeAsset


class ProfileService:
    def get_profile(self, session: Session) -> CandidateProfile | None:
        return session.scalars(select(CandidateProfile).limit(1)).first()

    def upsert_profile(self, session: Session, profile_json: dict) -> CandidateProfile:
        profile = self.get_profile(session)
        if profile is None:
            profile = CandidateProfile(profile_json=profile_json)
        else:
            profile.profile_json = profile_json
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile

    def list_answers(self, session: Session) -> list[AnswerLibrary]:
        return list(session.scalars(select(AnswerLibrary).order_by(AnswerLibrary.answer_key)).all())

    def create_answer(self, session: Session, payload: dict) -> AnswerLibrary:
        answer = AnswerLibrary(
            answer_key=payload["answer_key"],
            category=payload["category"],
            prompt_patterns_json=payload.get("prompt_patterns", []),
            answer_text=payload["answer_text"],
            requires_human_review=payload.get("requires_human_review", False),
            active=payload.get("active", True),
        )
        session.add(answer)
        session.commit()
        session.refresh(answer)
        return answer

    def update_answer(self, session: Session, answer_id: str, payload: dict) -> AnswerLibrary | None:
        answer = session.get(AnswerLibrary, answer_id)
        if answer is None:
            return None
        answer.category = payload.get("category", answer.category)
        answer.prompt_patterns_json = payload.get("prompt_patterns", answer.prompt_patterns_json)
        answer.answer_text = payload.get("answer_text", answer.answer_text)
        answer.requires_human_review = payload.get("requires_human_review", answer.requires_human_review)
        answer.active = payload.get("active", answer.active)
        session.add(answer)
        session.commit()
        session.refresh(answer)
        return answer

    def list_resumes(self, session: Session) -> list[ResumeAsset]:
        return list(session.scalars(select(ResumeAsset).order_by(ResumeAsset.variant_name)).all())

    def create_resume(self, session: Session, payload: dict) -> ResumeAsset:
        resume = ResumeAsset(
            variant_name=payload["variant_name"],
            file_path=payload["file_path"],
            active=payload.get("active", True),
            metadata_json=payload.get("metadata_json", {}),
        )
        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume
