from enum import StrEnum


class SourceType(StrEnum):
    COMPANY = "company"
    ATS = "ats"
    HTML = "html"
    FEED = "feed"


class RoleFamily(StrEnum):
    SWE = "swe"
    QUANT = "quant"
    BOTH = "both"
    OTHER = "other"


class ExperienceLevel(StrEnum):
    NEW_GRAD = "new_grad"
    ENTRY = "entry"
    ASSOCIATE = "associate"
    MID = "mid"
    SENIOR = "senior"
    UNKNOWN = "unknown"


class RemotePolicy(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


class JobStatus(StrEnum):
    NEW = "new"
    ACTIVE = "active"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class DecisionClass(StrEnum):
    AUTO_APPLY_NOW = "AUTO_APPLY_NOW"
    QUEUE_FOR_REVIEW = "QUEUE_FOR_REVIEW"
    ALERT_ONLY = "ALERT_ONLY"
    IGNORE = "IGNORE"
    RETRY_LATER = "RETRY_LATER"


class ApplicationStatus(StrEnum):
    PENDING = "PENDING"
    FORM_OPENED = "FORM_OPENED"
    RESUME_UPLOADED = "RESUME_UPLOADED"
    FIELDS_FILLED = "FIELDS_FILLED"
    VALIDATED = "VALIDATED"
    SUBMITTED = "SUBMITTED"
    CONFIRMED = "CONFIRMED"
    FAILED_FORM_DETECTION = "FAILED_FORM_DETECTION"
    FAILED_UPLOAD = "FAILED_UPLOAD"
    FAILED_VALIDATION = "FAILED_VALIDATION"
    FAILED_SUBMIT = "FAILED_SUBMIT"
    FAILED_CONFIRMATION = "FAILED_CONFIRMATION"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"


class SortMode(StrEnum):
    BEST_OVERALL = "best_overall"
    HIGHEST_PAY = "highest_pay"
    HIGHEST_PRESTIGE = "highest_prestige"
    BEST_QUANT = "best_quant"
    BEST_SWE = "best_swe"
    FASTEST_APPLY = "fastest_apply"
    BEST_REMOTE = "best_remote"


class OperatingMode(StrEnum):
    BALANCED = "balanced_mode"
    SWE_PRIORITY = "swe_priority_mode"
    QUANT_PRIORITY = "quant_priority_mode"

