from pathlib import Path

from packages.tracker.csv_sync import write_csv


def test_write_csv_creates_file_with_header_and_row(tmp_path: Path) -> None:
    target = tmp_path / "TopJobs.csv"
    write_csv(target, [{"company": "Google", "title": "Software Engineer"}])
    content = target.read_text()
    assert "company,title" in content
    assert "Google,Software Engineer" in content
