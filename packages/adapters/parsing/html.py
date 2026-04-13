from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    return BeautifulSoup(html, "lxml").get_text(" ", strip=True)

