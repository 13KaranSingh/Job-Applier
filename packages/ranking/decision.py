from packages.core.enums import DecisionClass
from packages.schemas.job import JobScoreSchema


def classify_decision(score: JobScoreSchema) -> DecisionClass:
    if score.recommended_action == DecisionClass.AUTO_APPLY_NOW.value:
        return DecisionClass.AUTO_APPLY_NOW
    if score.recommended_action == DecisionClass.QUEUE_FOR_REVIEW.value:
        return DecisionClass.QUEUE_FOR_REVIEW
    if score.recommended_action == DecisionClass.ALERT_ONLY.value:
        return DecisionClass.ALERT_ONLY
    if score.recommended_action == DecisionClass.RETRY_LATER.value:
        return DecisionClass.RETRY_LATER
    return DecisionClass.IGNORE

