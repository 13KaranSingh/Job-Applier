import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

JOB_LINK_PATTERNS = (
    re.compile(r"\bsoftware\b"),
    re.compile(r"\bengineer\b"),
    re.compile(r"\bfrontend\b"),
    re.compile(r"\bfront end\b"),
    re.compile(r"\bfull stack\b"),
    re.compile(r"\bbackend\b"),
    re.compile(r"\bquant\b"),
    re.compile(r"\btrader\b"),
    re.compile(r"\bresearcher\b"),
    re.compile(r"\bresearch engineer\b"),
    re.compile(r"\bdeveloper\b"),
    re.compile(r"\bswe\b"),
    re.compile(r"\bsde\b"),
)

NEGATIVE_LINK_TERMS = (
    "academy",
    "benefits",
    "blog",
    "contact",
    "culture",
    "customer",
    "demo",
    "documentation",
    "event",
    "foundation",
    "internship program",
    "learn",
    "login",
    "news",
    "open source",
    "overview",
    "partner",
    "platform overview",
    "podcast",
    "privacy",
    "product",
    "program",
    "research#",
    "security",
    "senior director",
    "principal",
    "staff",
    "manager",
    "sales",
    "account executive",
)

JOB_URL_HINTS = (
    "/jobs/",
    "/jobs/listing/",
    "/jobs/results/",
    "/position/",
    "/posting/",
    "/job/",
)


def extract_text(html: str) -> str:
    return BeautifulSoup(html, "lxml").get_text(" ", strip=True)


def extract_job_links(html: str, base_url: str, limit: int = 100) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    seen: set[str] = set()
    jobs: list[dict[str, str]] = []
    for anchor in soup.find_all("a", href=True):
        text = anchor.get_text(" ", strip=True)
        href = str(anchor["href"]).strip()
        if not text or not href:
            continue
        lowered = f"{text} {href}".lower()
        if not any(pattern.search(lowered) for pattern in JOB_LINK_PATTERNS):
            continue
        if not any(term in href.lower() for term in JOB_URL_HINTS):
            continue
        if any(term in lowered for term in NEGATIVE_LINK_TERMS):
            continue
        url = urljoin(base_url, href)
        if url in seen:
            continue
        seen.add(url)
        jobs.append({"title": text, "url": url})
        if len(jobs) >= limit:
            break
    return jobs
