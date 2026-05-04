from packages.adapters.ats.greenhouse import GreenhouseAdapter
from packages.adapters.ats.lever import LeverAdapter


def test_greenhouse_adapter_returns_empty_without_board_token() -> None:
    adapter = GreenhouseAdapter()
    assert adapter.config == {}


def test_lever_normalizes_role_family() -> None:
    adapter = LeverAdapter({"company_name": "Example"})
    job = adapter.normalize_job(
        {
            "id": "1",
            "text": "Quantitative Developer",
            "categories": {"location": "New York City"},
            "lists": [{"text": "Python C++ trading systems market microstructure"}],
            "hostedUrl": "https://jobs.example.com/1",
        }
    )
    assert job.role_family == "quant"
    assert job.company_name == "Example"
