"""This is module to parse CVPR specific page."""

import json
import logging
import pathlib
import time
from typing import Final

import requests
from bs4 import BeautifulSoup

from src.arxiv import get_arxiv_papers
from src.utils import PartialPaper, serialize_for_json_dump

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_papers(
    year: int,
    output_path: pathlib.Path,
    time_sleep: int = 1,
    save_frequency: int = 3,
) -> list[dict]:
    """Extract paper information from a list of URLs.

    In accepted papers page, a list of paper titles and authors are
    displayed. However, the abstract and other information are not.
    So try to find the paper from arxiv and if found, extract the
    abstract and urls from there.

    Args:
        year (int): The year of the conference.
        output_path (pathlib.Path): Output path to save the JSON file.
        time_sleep (int): Sleep time between requests.
        save_frequency (int): Save frequency of the papers.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    # Load papers from JSON file.
    if output_path.exists():
        with output_path.open("r") as f:
            papers: list[PartialPaper] = [
                PartialPaper.model_validate(p) for p in json.load(f)
            ]

        titles: set[str] = {paper.title.lower() for paper in papers}
        print(f"Papers loaded from {output_path}.")

    else:
        papers: list[PartialPaper] = []  # type: ignore[no-redef]
        titles: set[str] = set()  # type: ignore[no-redef]

    # Get title and authors from the accepted papers page.
    partial_papers = get_partial_papers(year)

    # Try to find the paper abstract and urls from arxiv.
    found_count: int = 0
    for i, partial_paper in enumerate(partial_papers):
        # Save the paper to the list.
        if (i + 1) % save_frequency == 0:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open("w") as f:
                json.dump(
                    [paper.model_dump() for paper in papers],
                    f,
                    indent=4,
                    default=serialize_for_json_dump,
                )

        logger.info(f"Processing {i+1}/{len(partial_papers)}: {partial_paper.title}")

        query = partial_paper.title.lower()
        # Skip if the paper is already found.
        if query in titles:
            found_count += 1
            continue
        else:
            # Sleep to avoid being blocked.
            time.sleep(time_sleep)

        paper = partial_paper
        for candidate_paper in get_arxiv_papers(query):
            # Check if the title and first author are the same.
            has_same_title = (
                candidate_paper.title.lower() == partial_paper.title.lower()
            )
            has_same_first_author = (
                candidate_paper.author.split(",")[0].lower()
                == partial_paper.author.split(",")[0].lower()
            )
            if has_same_title and has_same_first_author:
                found_count += 1
                paper = PartialPaper(
                    title=partial_paper.title,
                    author=partial_paper.author,
                    abstract=candidate_paper.abstract,
                    page=candidate_paper.page,
                    pdf=candidate_paper.pdf,
                )

        papers.append(paper)

    print(f"{found_count} / {len(partial_papers)} papers found in arxiv.")
    return [paper.model_dump() for paper in papers]


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
    papers = get_papers(
        year=2024,
        output_path=pathlib.Path("./data/json/cvpr2024_papers.json"),
    )
    print(papers)
