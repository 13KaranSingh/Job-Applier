from packages.adapters.generic import GenericCareersAdapter


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
