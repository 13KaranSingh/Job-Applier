from packages.adapters.companies.jane_street import JaneStreetAdapter


def test_jane_street_adapter_normalizes_job() -> None:
    adapter = JaneStreetAdapter()
    job = adapter.normalize_job(
        {
            "id": 123,
            "position": "Software Engineer",
            "category": "Technology",
            "availability": "Full-Time: Experienced",
            "city": "NYC",
            "overview": "<p>Build trading systems with Python, OCaml, and C++.</p>",
            "team": "Software Engineering",
            "duration": "Permanent",
            "min_salary": "250,000",
            "max_salary": "300,000",
        }
    )

    assert job.company_name == "Jane Street"
    assert job.company_type == "quant"
    assert job.location_raw == "New York, NY"
    assert job.role_family in {"swe", "quant", "both"}
    assert job.base_salary_min_usd == 250000
    assert job.base_salary_max_usd == 300000
    assert job.detail_url.endswith("/123/")


def test_jane_street_adapter_expands_split_city_codes() -> None:
    adapter = JaneStreetAdapter()
    job = adapter.normalize_job(
        {
            "id": 456,
            "position": "Quantitative Researcher",
            "category": "Trading",
            "availability": "Full-Time: Campus",
            "city": "NYC/HKG",
            "overview": "<p>Use probability, statistics, and market microstructure.</p>",
            "team": "Trading",
            "duration": "Permanent",
        }
    )

    assert job.location_raw == "New York, NY / Hong Kong"
    assert job.role_family == "quant"
