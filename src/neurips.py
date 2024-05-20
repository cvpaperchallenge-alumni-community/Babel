"""

This script generate json file which includes all papers information
of the selected conference. The code estimates NeurIPS proceedings page.
https://papers.nips.cc/

"""

import logging
from typing import Final

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
    pass


def get_paper_page_urls(conference: str, year: int) -> list[str]:
    """Return a list of NeurIPS proceedings page URL.

    Args:
        conference (str): The conference name.
        year (int): The year of the conference.

    Returns:
        list[str]: A list of NeurIPS proceedings page URL of each paper.
    """
    pass

def parse_paper_page(page_url: str) -> Paper:
    """Parse a paper page and return Paper object.

    Args:
        page_url (str): The URL of the paper page. The page url structure is like
            https://openaccess.thecvf.com/content/<conference_name><year>/html/<family_name>_<paper_title>_<conference_name>_<year>_paper.html

    Returns:
        Paper: The Paper object which stores the paper information.
    """
    pass


if __name__ == "__main__":
    paper = parse_paper_page(
        "https://papers.nips.cc/paper_files/paper/2023/hash/0001ca33ba34ce0351e4612b744b3936-Abstract-Conference.html"
    )
    print(paper.json())