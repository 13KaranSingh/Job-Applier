import re
from hashlib import sha256

from packages.core.constants import NEGATIVE_KEYWORDS, QUANT_POSITIVE_KEYWORDS, SWE_POSITIVE_KEYWORDS


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned


def normalize_company(company: str) -> str:
    return re.sub(r"\s+", " ", company).strip()


def normalize_title(title: str) -> str:
    title = title.lower().replace("/", " ")
    title = re.sub(r"[^a-z0-9+ ]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def normalize_location(location: str) -> str:
    location = location.strip()
    if not location:
        return "Unknown"
    aliases = {"nyc": "New York City", "sf": "San Francisco Bay Area", "remote us": "Remote"}
    return aliases.get(location.lower(), location)


def classify_role_family(title: str, description: str = "") -> str:
    haystack = f"{title} {description}".lower()
    has_swe = any(keyword in haystack for keyword in SWE_POSITIVE_KEYWORDS)
    has_quant = any(keyword in haystack for keyword in QUANT_POSITIVE_KEYWORDS)
    if has_swe and has_quant:
        return "both"
    if has_quant:
        return "quant"
    if has_swe:
        return "swe"
    return "other"


def classify_experience_level(title: str, description: str = "") -> str:
    haystack = f"{title} {description}".lower()
    if any(token in haystack for token in ["new grad", "university", "graduate", "entry level", "early career"]):
        return "new_grad"
    if any(token in haystack for token in ["0-2", "1-3", "associate", "swe i"]):
        return "entry"
    if any(token in haystack for token in ["2-4", "3-5", "swe ii"]):
        return "associate"
    if any(token in haystack for token in ["4-5", "5 years", "mid-level"]):
        return "mid"
    if any(token in haystack for token in NEGATIVE_KEYWORDS):
        return "senior"
    return "unknown"


def canonical_job_key(company: str, title: str, location: str, external_id: str | int | None = None) -> str:
    raw = "|".join(
        [
            slugify(company),
            slugify(title),
            slugify(location),
            str(external_id or ""),
        ]
    )
    return sha256(raw.encode("utf-8")).hexdigest()

