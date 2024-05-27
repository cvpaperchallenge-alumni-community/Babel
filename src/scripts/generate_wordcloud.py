"""Generate word cloud image from paper title and abstract."""

import csv
import json
import pathlib
from typing import Final, Set

from wordcloud import WordCloud

from src.utils import Paper


def generate_wordcloud_from_json(
    json_path: pathlib.Path,
    image_save_path: pathlib.Path,
    stopwords: Set[str],
    seed: int,
    use_abstract: bool = False,
) -> None:
    """Generate word cloud. All features like Tokenizer or Lemmatizer
    are comming from WordCloud library.

    Args:
        json_path (pathlib.Path): Path to the JSON file which
            includes paper information.
        image_save_path (pathlib.Path): Path to save the generated word
            cloud image.
        stopwords (Set[str]): Set of stopwords.
        seed (int): Random seed for reproducibility.
        use_abstract (bool): Whether to use abstract in addition to
            title. Defaults to False.

    """
    # Load papers from JSON file.
    with json_path.open("r") as f:
        papers: list[Paper] = [Paper.model_validate(p) for p in json.load(f)]

    # Concat all titles and abstructs.
    all_title = " ".join([paper.title for paper in papers])
    all_abstract = " ".join([paper.abstract for paper in papers])
    source_text = all_title + " " + all_abstract if use_abstract else all_title

    wordcloud: Final = WordCloud(
        width=1600,
        height=800,
        max_font_size=120,
        min_font_size=12,
        background_color="black",
        stopwords=stopwords,
        random_state=seed,
    ).generate(source_text)
    wordcloud.to_file(str(image_save_path))

    print(f"Word cloud image is saved at {image_save_path}.")


def generate_wordcloud_from_csv(
    csv_path: pathlib.Path,
    image_save_path: pathlib.Path,
    seed: int,
) -> None:
    """Generate word cloud from CSV file.

    Args:
        csv_path (pathlib.Path): Path to the CSV file which includes
            text data.
        image_save_path (pathlib.Path): Path to save the generated word
            cloud image.
        seed (int): Random seed for reproducibility.

    """
    # Load frequency data from CSV file.
    with csv_path.open("r") as f:
        reader = csv.reader(f)
        _ = next(reader)  # Skip header.
        frequency_dict: dict[str, int] = {row[0]: int(row[1]) for row in reader}

    # Generate word cloud.
    wordcloud: Final = WordCloud(
        width=1600,
        height=800,
        max_font_size=120,
        min_font_size=12,
        background_color="black",
        random_state=seed,
    )
    wordcloud.generate_from_frequencies(frequency_dict)
    wordcloud.to_file(str(image_save_path))

    print(f"Word cloud image is saved at {image_save_path}.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-path",
        "-i",
        type=pathlib.Path,
        help="An input JSON/CSV file path.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=pathlib.Path,
        default="./outputs/wordcloud",
        help="Output directory to save generated wordcloud image.",
    )
    parser.add_argument(
        "--stopwords-path",
        type=pathlib.Path,
        default="./data/stopwords.txt",
        help="A txt file which includes stopwords.",
    )
    parser.add_argument(
        "--seed",
        "-s",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
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

    # Create output directory if not exists.
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.input_path.suffix == ".csv":
        generate_wordcloud_from_csv(
            args.input_path,
            args.output_dir / f"{args.input_path.stem}_seed={args.seed}.png",
            args.seed,
        )

    elif args.input_path.suffix == ".json":
        # Load stopwords.
        stopwords = set()
        with args.stopwords_path.open("r") as f:
            for line in f:
                stopwords.add(line.strip())

        generate_wordcloud_from_json(
            args.input_path,
            args.output_dir / f"{args.input_path.stem}_seed={args.seed}.png",
            stopwords,
            args.seed,
            args.use_abstract,
        )

    else:
        raise ValueError(f"Unsupported file type: {args.input_path.suffix}")
