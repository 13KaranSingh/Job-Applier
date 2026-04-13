from packages.source_seeding.seed_loader import build_default_sources


def test_build_default_sources_includes_ats_and_company_boards() -> None:
    sources = build_default_sources()
    slugs = {source["slug"] for source in sources}
    assert "greenhouse" in slugs
    assert "lever" in slugs
    assert "google" in slugs
