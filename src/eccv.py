import logging
from typing import Final

import requests
from bs4 import BeautifulSoup

from src.utils import Paper

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_papers(year: int) -> list[dict]:
    """Extract paper information from a list of URLs.

    Args:
        year (int): The year of the conference.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    urls: Final[list[str]] = get_paper_page_urls(year=year)

    papers: list[dict] = list()
    for i, url in enumerate(urls):
        logger.info(f"Processing {i+1}/{len(urls)}: {url}")
        paper = parse_paper_page(url)
        papers.append(paper.model_dump())

    return papers


def get_paper_page_urls(year: int) -> list[str]:
    """Return a list of single paper page URL.

    The page contains information about the papers over several years,
    but the year info in the URL is used to narrow down like following.
    e.g. papers/eccv_2022/papers_ECCV/html/19_ECCV_2022_paper.php

    Args:
        year (int): The year of the conference.

    Returns:
        list[str]: A list of the page URL of each paper.

    """
    root_url: Final[str] = "https://www.ecva.net/papers.php"

    html: Final[str] = requests.get(root_url).text
    bs: Final = BeautifulSoup(html, "html.parser")

    # This list inludes sub-URLs like "papers/eccv_2022/papers_ECCV/html/19_ECCV_2022_paper.php".
    all_paper_page_sub_urls: list[str] = [
        link.get("href") for link in bs.select("dt.ptitle a") if link.get("href")
    ]

    return [
        root_url.replace("papers.php", "") + url
        for url in all_paper_page_sub_urls
        if f"eccv_{year}" in url
    ]


def parse_paper_page(page_url: str) -> Paper:
    """Parse a paper page and return Paper object.

    Args:
        page_url (str): The URL of the paper page. The page url is like
            https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/19_ECCV_2022_paper.php

    Returns:
        Paper: The Paper object which stores the paper information.

    """
    html: Final[str] = requests.get(page_url).text
    bs: Final = BeautifulSoup(html, "html.parser")

    title = bs.find(id="papertitle").text.strip()
    author = bs.find(id="authors").text.replace(";", "").strip()
    abstract = bs.find(id="abstract").text.strip().strip('"')
    sub_pdf_url = bs.find("a", href=True, text="pdf").get("href")
    root_url: Final[str] = "https://www.ecva.net/papers.php"
    pdf = root_url.replace("papers.php", "") + sub_pdf_url.replace("../../../../", "")

    return Paper(
        title=title,
        author=author,
        abstract=abstract,
        page=page_url,  # type: ignore
        pdf=pdf,
    )


if __name__ == "__main__":
    paper = parse_paper_page(
        "https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/19_ECCV_2022_paper.php"
    )
    print(paper.json())
