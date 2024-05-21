"""This script generate json file which includes all papers information of the selected conference.
The code estimates Computer Vision Foundation(CVF) supported conferences such as CVPRWS.

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

    papers: list[dict] = list()
    for i, url in enumerate(urls):
        logger.info(f"Processing {i+1}/{len(urls)}: {url}")
        paper = parse_paper_page(url)
        papers.append(paper.model_dump())

    return papers


def get_paper_page_urls(conference: str, year: int) -> list[str]:
    """Return a list of CVF page URL.

    The number of accepted papers is different for each conference:
        - CVPRWS 2023: 697 papers
        - CVPRWS 2022: 561 papers

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        list[str]: A list of CVF page URL of each paper.
    """
    cvf_root_url: Final[str] = "https://openaccess.thecvf.com"
    conference_name: Final[str] = validate_conference(conference, year)

    # まず、ルートのページでは開催されるWorkshopのページ一覧が表示される
    # https://openaccess.thecvf.com/CVPR2023_workshops/menu
    ws_root_url: Final = cvf_root_url + f"/{conference_name}_workshops/menu"

    html: Final = requests.get(ws_root_url).text
    bs: Final = BeautifulSoup(html, "html.parser")
    parsed_tags = bs.select("#content a")
    # workshopごとのページに遷移するためのURLを取得する
    # https://openaccess.thecvf.com/CVPR2023_workshops/TCV
    ws_root_list = [cvf_root_url + parsed_tag.get("href") for parsed_tag in parsed_tags]
    ws_all_paper_url_list = []
    for ws_root in ws_root_list:
        ws_html = requests.get(ws_root).text
        ws_bs = BeautifulSoup(ws_html, "html.parser")
        ws_parsed_tags = ws_bs.select(".ptitle > a")
        a = [
            cvf_root_url + ws_parsed_tag.get("href") for ws_parsed_tag in ws_parsed_tags
        ]
        ws_all_paper_url_list.extend(a)
    return ws_all_paper_url_list


def validate_conference(conference: str, year: int) -> str:
    """Validate the user specified conference name and year and return
    the unique conference name with year.

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        str: The unique conference name with year.
    """
    if conference == "cvprw":
        if year not in range(2019, 2023):
            raise ValueError(
                "CVPRWS conference is held from 2019 to 2023. \
                Please specify the year in the range."
            )
        return f"CVPR{year}"
    else:
        raise ValueError(
            f"You specified the conference name as {conference}, \
            but our code does not support the conference."
        )


def parse_paper_page(page_url: str) -> Paper:
    """Parse a paper page and return Paper object.

    Args:
        page_url (str): The URL of the paper page. The page url structure is like
            https://openaccess.thecvf.com/content/<conference_name><year>W/<workshop_name>/html/<family_name>_<paper_title>_<conference_name>W_<year>_paper.html
            "W" means Workshop.

    Returns:
        Paper: The Paper object which stores the paper information.
    """
    html: Final[str] = requests.get(page_url).text
    bs: Final = BeautifulSoup(html, "html.parser")

    title: Final[str] = (
        bs.select_one("#papertitle").text.strip()
        if bs.select_one("#papertitle") is not None
        else ""
    )
    author: Final[str] = (
        bs.select_one("#authors b").text.strip()
        if bs.select_one("#authors b") is not None
        else ""
    )
    abstract: Final[str] = (
        bs.select_one("#abstract").text.strip()
        if bs.select_one("#abstract") is not None
        else ""
    )
    page: Final[str] = page_url

    # conference_path is like: https://openaccess.thecvf.com/content/CVPR2023W/<workshop_name>
    conference_path: Final[str] = "/".join(page_url.split("/", 6)[:6])
    print(conference_path)
    # paper_name is like: <family_name>_<paper_title>_<conference_name>_<year>_paper
    paper_name: Final[str] = page_url.rsplit("/", 1)[1].removesuffix(".html")
    pdf: Final[str] = conference_path + "/papers/" + paper_name + ".pdf"

    return Paper(
        title=title,
        author=author,
        abstract=abstract,
        page=page,  # type: ignore
        pdf=pdf,  # type: ignore
    )


if __name__ == "__main__":
    paper = parse_paper_page(
        "https://openaccess.thecvf.com/content/CVPR2023W/TCV/html/Gowda_Synthetic_Sample_Selection_for_Generalized_Zero-Shot_Learning_CVPRW_2023_paper.html"
    )
    print(paper.json())
