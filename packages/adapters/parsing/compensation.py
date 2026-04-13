import re
from dataclasses import dataclass


@dataclass(slots=True)
class CompensationParseResult:
    base_salary_min_usd: float | None
    base_salary_max_usd: float | None
    hourly_rate_min_usd: float | None
    hourly_rate_max_usd: float | None
    compensation_frequency: str
    compensation_confidence: float
    bonus_text: str | None = None
    equity_text: str | None = None


MONEY_PATTERN = re.compile(r"\$?(\d{2,3}(?:,\d{3})*(?:\.\d+)?)")


def parse_compensation(text: str | None) -> CompensationParseResult:
    if not text:
        return CompensationParseResult(None, None, None, None, "unknown", 0.0)
    values = [float(value.replace(",", "")) for value in MONEY_PATTERN.findall(text)]
    lowered = text.lower()
    if "hour" in lowered:
        if len(values) >= 2:
            return CompensationParseResult(None, None, values[0], values[1], "hourly", 0.8)
        if len(values) == 1:
            return CompensationParseResult(None, None, values[0], values[0], "hourly", 0.6)
    if len(values) >= 2:
        return CompensationParseResult(values[0], values[1], None, None, "annual", 0.9)
    if len(values) == 1:
        return CompensationParseResult(values[0], values[0], None, None, "annual", 0.6)
    return CompensationParseResult(None, None, None, None, "unknown", 0.0)

