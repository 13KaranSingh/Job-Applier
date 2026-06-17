from packages.adapters.generic import GenericCareersAdapter
from packages.adapters.parsing.html import extract_job_links


def test_generic_adapter_normalizes_jsonld_job() -> None:
    adapter = GenericCareersAdapter({"company_name": "Example AI", "career_url": "https://example.com/jobs"})
    job = adapter.normalize_job(
        {
            "@type": "JobPosting",
            "title": "Software Engineer",
            "description": "<p>Python React TypeScript product engineering</p>",
            "url": "https://example.com/jobs/1",
            "jobLocation": {"address": {"addressLocality": "New York", "addressRegion": "NY"}},
        }
    )
    assert job.company_name == "Example AI"
    assert job.role_family == "swe"
    assert job.location_normalized == "New York, NY"


def test_extract_job_links_finds_relevant_roles() -> None:
    html = """
    <html><body>
      <a href="/jobs/software-engineer-new-grad">Software Engineer, New Grad</a>
      <a href="/jobs/account-executive">Account Executive</a>
      <a href="/jobs/quant-trader">Quantitative Trader</a>
    </body></html>
    """

    links = extract_job_links(html, "https://careers.example.com")

    assert links == [
        {
            "title": "Software Engineer, New Grad",
            "url": "https://careers.example.com/jobs/software-engineer-new-grad",
        },
        {
            "title": "Quantitative Trader",
            "url": "https://careers.example.com/jobs/quant-trader",
        },
    ]
