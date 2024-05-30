"""This is module to parse CVPR specific page."""

import logging
from typing import Final

import requests
from bs4 import BeautifulSoup

from src.arxiv import get_arxiv_papers
from src.utils import PartialPaper

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_papers(year: int) -> list[dict]:
    """Extract paper information from a list of URLs.

    In accepted papers page, a list of paper titles and authors are
    displayed. However, the abstract and other information are not.
    So try to find the paper from arxiv and if found, extract the
    abstract and urls from there.

    Args:
        year (int): The year of the conference.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    # Get title and authors from the accepted papers page.
    partial_papers = get_partial_papers(year)

    # Try to find the paper abstract and urls from arxiv.
    found_count: int = 0
    for i, paper in enumerate(partial_papers):
        logger.info(f"Processing {i+1}/{len(partial_papers)}: {paper.title}")

        query = f"{paper.title}".lower()
        for candidate_paper in get_arxiv_papers(query):
            # Check if the title and first author are the same.
            has_same_title = candidate_paper.title.lower() == paper.title.lower()
            has_same_first_author = (
                candidate_paper.author.split(",")[0].lower()
                == paper.author.split(",")[0].lower()
            )
            if has_same_title and has_same_first_author:
                paper.abstract = candidate_paper.abstract
                paper.pdf = candidate_paper.pdf
                paper.page = candidate_paper.page
                found_count += 1
                break

    print(f"{found_count} / {len(partial_papers)} papers found in arxiv.")
    return [paper.model_dump() for paper in partial_papers]


def get_partial_papers(year: int) -> list[PartialPaper]:
    """Get partial papers from the CVPR accepted papers page.

    Args:
        year (int): The year of the conference.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    url: Final = f"https://cvpr.thecvf.com/Conferences/{year}/AcceptedPapers"

    html = requests.get(url).text
    bs = BeautifulSoup(html, "html.parser")

    # hypothesys that the title and author are in the table.
    table = bs.find("table")

    partial_papers: list[PartialPaper] = []
    rows = table.find_all("tr")
    for i, row in enumerate(rows):
        # Skip first two blank rows.
        if i < 2:
            continue

        # Find title.
        title_tag = row.find("a")
        if title_tag:
            title = title_tag.text.strip()
        else:
            title_tag = row.find("strong")
            if not title_tag:
                raise ValueError("Title not found")

            title = title_tag.text.strip()

        # Find author.
        author_tag = row.find("div", class_="indented")
        if not author_tag:
            raise ValueError("Authors not found.")
        author = author_tag.find("i").text.strip()
        author = author.replace(" · ", ", ")

        partial_papers.append(
            PartialPaper(
                title=title,
                author=author,
            )
        )

    return partial_papers


if __name__ == "__main__":
    papers = get_papers(2024)
    print(papers)
