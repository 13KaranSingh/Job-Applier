from packages.adapters.parsing.normalization import canonical_job_key


def test_canonical_job_key_matches_same_job_inputs() -> None:
    left = canonical_job_key("Google", "Software Engineer", "New York City", "123")
    right = canonical_job_key("Google", "Software Engineer", "New York City", "123")
    assert left == right

