if __name__ == "__main__":
    import argparse
    import csv
    import pathlib
    from typing import Final

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-path",
        "-i",
        type=pathlib.Path,
        help="An input CSV file path.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=pathlib.Path,
        default="./outputs/adjusted_frequency/",
        help="Output directory to save generated wordcloud image.",
    )
    parser.add_argument(
        "--stopwords-path",
        type=pathlib.Path,
        default="./data/exact_match_stopwords.txt",
        help="A txt file which includes exact match stopwords.",
    )
    parser.add_argument(
        "--minimum-count",
        "-m",
        type=int,
        default=6,
        help="Minimum count of n-gram to be included in the result.",
    )
    args = parser.parse_args()

    # Load stopwords.
    stopwords = set()
    with args.stopwords_path.open("r") as f:
        for line in f:
            stopwords.add(line.strip())

    # Check if input file exists.
    if not args.input_path.exists():
        raise FileNotFoundError(f"{args.input_path} does not exist.")

    # Specify output path.
    output_path: Final = (
        args.output_dir
        / args.input_path.parent.stem
        / f"{args.input_path.stem}_adjusted.csv"
    )
    # Create output directory if not exists.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load frequency data from CSV file.
    with args.input_path.open("r") as f:
        reader = csv.reader(f)
        header = next(reader)
        frequency_dict: dict[str, int] = {row[0]: int(row[1]) for row in reader}

    # Remove n-grams whose count is less than the minimum count.
    adjusted_frequency_dict = {
        k: v for k, v in frequency_dict.items() if v >= args.minimum_count
    }

    # Remove stopwords from frequency data.
    adjusted_frequency_dict = {
        k: v for k, v in adjusted_frequency_dict.items() if k.lower() not in stopwords
    }

    # Save word frequency as CSV file.
    with output_path.open("w", newline="") as f:
        writer: Final = csv.writer(f)
        writer.writerow(["word", "count"])
        for key, value in adjusted_frequency_dict.items():
            writer.writerow([key, value])

    print(f"Adjusted word frequency is saved as {output_path}.")
