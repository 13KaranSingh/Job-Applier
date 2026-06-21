from packages.adapters.companies.google import GoogleAdapter


def test_google_adapter_extracts_jobs_from_inline_html() -> None:
    adapter = GoogleAdapter({"career_url": "https://www.google.com/about/careers/applications/jobs/results/"})
    html = r'''
    ["12345","Software Engineer, Early Career","https://www.google.com/about/careers/applications/signin?jobId=abc123",null,null,"Google","en-US",[["New York, NY, USA"]],[null,"Build systems with Python. US: $140000 - $200000 (USD)"]]
    ["67890","Quantitative Analyst","https://www.google.com/about/careers/applications/signin?jobId=def456",null,null,"Google","en-US",[["Chicago, IL, USA"]],[null,"Analyze models. US: $150000 - $220000 (USD)"]]
    '''

    jobs = adapter.extract_jobs_from_html(html)

    assert len(jobs) == 2
    assert jobs[0]["id"] == "12345"
    assert jobs[0]["title"] == "Software Engineer, Early Career"
    assert jobs[0]["location"] == "New York, NY, USA"


def test_google_adapter_normalizes_job() -> None:
    adapter = GoogleAdapter()
    job = adapter.normalize_job(
        {
            "id": "12345",
            "title": "Software Engineer, Early Career",
            "apply_url": "https://www.google.com/about/careers/applications/signin?jobId=abc123",
            "company_name": "Google",
            "location": "New York, NY, USA",
            "description": "Build systems. US: $140,000 - $200,000 (USD)",
        }
    )

    assert job.company_name == "Google"
    assert job.role_family == "swe"
    assert job.base_salary_min_usd == 140000
