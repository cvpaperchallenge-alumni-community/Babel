"""Caluculate word frequency and save it as CSV file."""

if __name__ == "__main__":
    import argparse
    import csv
    import json
    import pathlib
    from typing import Final

    from src.utils import Paper
    from src.word_frequency import calculate_word_frequency, sort_frequency_dict

    # Parse command line arguments.
    parser: Final = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path",
        "-i",
        type=pathlib.Path,
        help="An input JSON file path.",
    )
    parser.add_argument(
        "--use-abstract",
        action="store_true",
        help="Use abstracts in addition to titles.",
    )
    args = parser.parse_args()

    # Check if input file exists.
    if not args.input_path.exists():
        raise FileNotFoundError(f"{args.input_path} does not exist.")

    # Specify output path.
    output_root_dir: Final = pathlib.Path("./outputs/raw_frequency/")
    if args.use_abstract:
        output_path: pathlib.Path = (
            output_root_dir
            / "title_and_abstract"
            / f"{args.input_path.stem}_title_and_abstract.csv"
        )
    else:
        output_path: pathlib.Path = (  # type: ignore[no-redef]
            output_root_dir / "title_only" / f"{args.input_path.stem}_title_only.csv"
        )

    # Create output directory if not exists.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load papers from JSON file.
    with args.input_path.open("r") as f:
        papers: list[Paper] = [Paper.model_validate(p) for p in json.load(f)]

    # Concat all titles and abstructs.
    all_title = " ".join([paper.title for paper in papers])
    all_abstract = " ".join([paper.abstract for paper in papers])
    source_text = all_title + " " + all_abstract if args.use_abstract else all_title

    # Calculate word frequency.
    frequency_dict = sort_frequency_dict(calculate_word_frequency(source_text))

    # Save word frequency as CSV file.
    with output_path.open("w", newline="") as f:
        writer: Final = csv.writer(f)
        writer.writerow(["word", "count"])
        for key, value in frequency_dict.items():
            writer.writerow([key, value])
