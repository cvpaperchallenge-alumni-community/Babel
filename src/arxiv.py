import re
from typing import Final
from xml.etree import ElementTree

import requests

from src.utils import Paper


def get_arxiv_papers(
    query: str,
    max_results: int = 3,
) -> list[Paper]:
    """Get papers from arXiv API.

    Args:
        query (str): The query to search papers.
        max_results (int): The maximum number of papers to get. Defaults to 3.

    Returns:
        list[Paper]: A list of Paper objects.

    """
    # Define the URL.
    base_url: Final = "http://export.arxiv.org/api/query"
    search_query: Final = f"search_query={query}&start=0&max_results={max_results}"
    url: Final = f"{base_url}?{search_query}"

    # Get the response from the URL.
    response: Final = requests.get(url)

    # Check the response status code.
    if response.status_code != 200:
        raise ValueError(
            f"Failed to get the response from {url}. The status code is {response.status_code}."
        )

    # Parse the response content.
    root: Final = ElementTree.fromstring(response.content)

    papers: list[Paper] = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title: str = clean_text(entry.find("{http://www.w3.org/2005/Atom}title").text)  # type: ignore
        summary: str = clean_text(
            entry.find("{http://www.w3.org/2005/Atom}summary").text  # type: ignore
        )
        id_url: str = entry.find("{http://www.w3.org/2005/Atom}id").text  # type: ignore

        # page_url is url like "http://arxiv.org/abs/2305.11288v2".
        # We need to extract the id like "2305.11288".
        arxiv_id: str = id_url.split("/")[-1].split("v")[0]
        arxiv_url: str = f"http://arxiv.org/abs/{arxiv_id}"
        pdf_url: str = f"http://arxiv.org/pdf/{arxiv_id}.pdf"

        # Get authors.
        authors: list[str] = []
        for author in entry.findall("{http://www.w3.org/2005/Atom}author"):
            name: str = author.find("{http://www.w3.org/2005/Atom}name").text  # type: ignore
            authors.append(name)

        paper = Paper(
            title=title,
            author=", ".join(authors),
            abstract=summary,
            page=arxiv_url,  # type: ignore
            pdf=pdf_url,  # type: ignore
        )
        papers.append(paper)

    return papers


def clean_text(text: str) -> str:
    """Remove newline or extra spaces from the text.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.

    """
    # Remove \n from the text.
    text = re.sub(r"\n", " ", text)
    # Remove extra spaces from the text.
    cleaned_text = re.sub(r"\s+", " ", text).strip()
    return cleaned_text


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        help="An input query to search papers on arXiv.",
    )
    args = parser.parse_args()

    papers = get_arxiv_papers(args.query)
    print(papers)
