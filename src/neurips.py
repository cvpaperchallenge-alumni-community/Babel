"""This script generate json file which includes all papers information of the selected conference.
The code estimates Computer Vision Foundation(CVF) supported conferences such as CVPR and ICCV.

"""

import logging
from typing import Final

import requests
from bs4 import BeautifulSoup

from src.utils import Paper

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_papers(conference: str, year: int) -> list[dict]:
    """Extract paper information from a list of URLs.

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    urls: Final[list[str]] = get_paper_page_urls(conference=conference, year=year)
    print(f"urls:{urls}")

    papers: list[dict] = list()
    for i, url in enumerate(urls):
        logger.info(f"Processing {i+1}/{len(urls)}: {url}")
        paper = parse_paper_page(url)
        papers.append(paper.model_dump())

    return papers


def get_paper_page_urls(conference: str, year: int) -> list[str]:
    """Return a list of CC page URL.

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        list[str]: A list of CC page URL of each paper.
    """
    cc_root_url: Final[str] = "https://papers.nips.cc"
    print(f"cc_root_url:{cc_root_url}")
    cc_all_paper_url: Final = cc_root_url + f"/paper_files/paper/{year}"
    print(f"cc_all_paper_url:{cc_all_paper_url}")

    html: Final = requests.get(cc_all_paper_url).text
    bs: Final = BeautifulSoup(html, "html.parser")
    if year == 2022 or year == 2023:
        parsed_tags = bs.select(
            "div.container-fluid div.col ul.paper-list li.conference a"
        )
    else:
        parsed_tags = bs.select("div.container-fluid div.col ul.paper-list li a")
    print(f"parsed_tags:{parsed_tags}")
    return [cc_root_url + parsed_tag.get("href") for parsed_tag in parsed_tags]


def validate_conference(conference: str, year: int) -> str:
    """Validate the user specified conference name and year and return
    the unique conference name with year.

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        str: The unique conference name with year.
    """
    if conference == "neurlips":
        if year not in range(2018, 2023):
            raise ValueError(
                "NeurIPS conference is held from 2019 to 2023. \
                Please specify the year in the range."
            )
        return f"NeurIPS{year}"
    else:
        raise ValueError(
            f"You specified the conference name as {conference}, \
            but our code does not support the conference."
        )


def parse_paper_page(page_url: str) -> Paper:
    """Parse a paper page and return Paper object.

    Args:
        page_url (str): The URL of the paper page. The page url structure is like
            https://papers.nips.cc/paper_files/paper/<year>/hash/0001ca33ba34ce0351e4612b744b3936-Abstract-Conference.html

    Returns:
        Paper: The Paper object which stores the paper information.
    """
    html: Final[str] = requests.get(page_url).text
    bs: Final = BeautifulSoup(html, "html.parser")

    title: Final[str] = (
        bs.select_one("div.container-fluid div.col h4").text.strip()
        if bs.select_one("div.container-fluid div.col h4") is not None
        else ""
    )
    author: Final[str] = (
        bs.select_one("div.container-fluid div.col h4 + p i").text.strip()
        if bs.select_one("div.container-fluid div.col h4 + p i") is not None
        else ""
    )
    abstract: Final[str] = (
        bs.select_one("div.container-fluid div.col h4 + p + h4 + p").text.strip()
        if bs.select_one("div.container-fluid div.col h4 + p + h4 + p") is not None
        else ""
    )
    page: Final[str] = page_url

    # conference_path is like: https://papers.nips.cc/paper_files/paper/<year>/hash/<paper_name>.html
    conference_path: Final[str] = "/".join(page_url.split("/", 6)[:6])
    print(conference_path)
    # paper_name is like: 0001ca33ba34ce0351e4612b744b3936-Abstract-Conference
    # or 01726ae05d72ddba3ac784a5944fa1ef-Abstract-Datasets_and_Benchmarks
    paper_name: str = page_url.rsplit("/", 1)[1].removesuffix(".html")
    # Abstruct-Conference -> Paper-Conference.
    if "Abstract" in paper_name:
        paper_name = paper_name.replace("Abstract", "Paper")
    pdf: Final[str] = conference_path + "/file/" + paper_name + ".pdf"

    return Paper(
        title=title,
        author=author,
        abstract=abstract,
        page=page,  # type: ignore
        pdf=pdf,  # type: ignore
    )


if __name__ == "__main__":
    paper = parse_paper_page(
        "https://papers.nips.cc/paper_files/paper/2023/hash/01726ae05d72ddba3ac784a5944fa1ef-Abstract-Datasets_and_Benchmarks.html"
    )
    print(paper.json())
