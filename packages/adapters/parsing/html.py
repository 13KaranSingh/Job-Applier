from urllib.parse import urljoin

from bs4 import BeautifulSoup

JOB_LINK_TERMS = (
    "software",
    "engineer",
    "frontend",
    "front end",
    "full stack",
    "backend",
    "platform",
    "infrastructure",
    "quant",
    "trader",
    "research",
    "developer",
    "trading",
)

NEGATIVE_LINK_TERMS = (
    "senior director",
    "principal",
    "staff",
    "manager",
    "sales",
    "account executive",
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
        if not any(term in lowered for term in JOB_LINK_TERMS):
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
