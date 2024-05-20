"""This script generate json file which includes all papers information of
the selected conference.
"""

import argparse
import json
import logging
import pathlib
from typing import Final, Iterable

from src import cvf, neurips
from src.utils import serialize_for_json_dump

logger: Final = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def scrape_conference_page(
    output_dir: pathlib.Path, conference: str, year: int
) -> None:
    """Scrape conference page to extract paper information and save it
    as JSON file. Output file name is `{conference}{year}_papers.json`.

    Args:
        output_dir (str): Output directory to save the JSON file.
        conference (str): The conference name.
        year (int): The year of the conference.

    """
    # Specify conference name and year.
    papers: Iterable[dict] = list()
    if conference in ["cvpr", "iccv"]:
        papers = cvf.get_papers(conference=conference, year=year)
    elif conference == "eccv":
        raise NotImplementedError("Not implemented yet.")
    elif conference == "neurips":
        papers = neurips.get_papers(conference=conference, year=year)
    elif conference == "cvprw":
        raise NotImplementedError("Not implemented yet.")
    else:
        raise ValueError(f"Conference {conference} is not supported.")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path: Final = output_dir / f"{conference}{year}_papers.json"
    with output_path.open("w") as f:
        json.dump(papers, f, indent=4, default=serialize_for_json_dump)

    logger.info(f"Successfully parsed {len(papers)} papers.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output-dir",
        "-o",
        type=pathlib.Path,
        default="./data/json",
        help="Output directory to save the JSON file.",
    )
    parser.add_argument(
        "--conference",
        "-c",
        choices=["cvpr", "iccv", "eccv", "neurips", "cvprw"],
        type=str,
        required=True,
        help="Conference name where papers information is extracted.",
    )
    parser.add_argument(
        "--year",
        "-y",
        type=int,
        required=True,
        help="The year of the conference.",
    )
    args = parser.parse_args()

    scrape_conference_page(
        output_dir=args.output_dir, conference=args.conference, year=args.year
    )
