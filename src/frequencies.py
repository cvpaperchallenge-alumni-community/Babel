import re
from collections import Counter
from typing import Final

import nltk
from nltk import ngrams
from nltk.corpus import stopwords


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove stopwords from the list of tokens.

    Args:
        tokens (list[str]): A list of tokens.

    Returns:
        list[str]: A list of tokens without stopwords.

    """
    nltk.download("stopwords")
    default_stopwords: Final = set(stopwords.words("english"))
    # Add custom stopwords
    custom_stopwords = set(
        "~ ` `` ! @ # $ % ^ & * ( ) _ + - = { } [ ] \\ | : ; ' '' < > , . ... ? / //".split()
        + ['"', '""']
    )
    custom_stopwords.update(default_stopwords)

    # If the token is a number, add it to the stop words.
    number_pattern = re.compile(r"^\d+$")
    custom_stopwords.update([token for token in tokens if number_pattern.match(token)])

    # If the token is a URL or special charactor, replace it with an empty string.
    tokens = [
        re.sub(r"http.*+|www.*|github.*|\\.*", "", token, flags=re.MULTILINE)
        for token in tokens
    ]

    # Filter out the tokens that are in the stop words or are empty.
    return [
        token
        for token in tokens
        if token.lower() not in custom_stopwords and token != "" and token.strip() != ""
    ]


def get_ngrams(tokens: list[str], n: int) -> dict:
    """Return the n-grams of the tokens.

    Args:
        tokens (list[str]): A list of tokens.
        n (int): The number of n-grams.

    Returns:
        dict: A dictionary of n-grams and their frequencies.

    """
    nltk.download("punkt")

    n_grams = ngrams(tokens, n)
    n_gram_freq = {" ".join(k): v for k, v in Counter(n_grams).items()}
    return n_gram_freq


def sort_frequency_dict(frequency_dict: dict[str, int]) -> dict[str, int]:
    """First, sort the dictionary by the values in descending order, and
    then sort the items with the same value by their keys in ascending
    order.

    Args:
        frequency_dict (dict[str, int]): A frequency dict.

    Returns:
        dict[str, int]: A sorted frequency dict.

    """
    return dict(sorted(frequency_dict.items(), key=lambda item: (-item[1], item[0])))


if __name__ == "__main__":
    text = "Current state-of-the-art semantic segmentation methods often apply high-resolution input to attain high performance, which brings large computation budgets and limits their applications on resource-constrained devices. In this paper, we propose a simple and flexible two-stream framework named Dual Super-Resolution Learning (DSRL) to effectively improve the segmentation accuracy without introducing extra computation costs. Specifically, the proposed method consists of three parts: Semantic Segmentation Super-Resolution (SSSR), Single Image Super-Resolution (SISR) and Feature Affinity (FA) module, which can keep high-resolution representations with low-resolution input while simultaneously reducing the model computation complexity. Moreover, it can be easily generalized to other tasks, e.g., human pose estimation. This simple yet effective method leads to strong representations and is evidenced by promising performance on both semantic segmentation and human pose estimation. Specifically, for semantic segmentation on CityScapes, we can achieve \\geq2% higher mIoU with similar FLOPs, and keep the performance with 70% FLOPs. For human pose estimation, we can gain \\geq2% mAP with the same FLOPs and maintain mAP with 30% fewer FLOPs. Code and models are available at https://github.com/wanglixilinx/DSRL."

    tokens = nltk.word_tokenize(text)
    filtered_tokens = remove_stopwords(tokens)

    print(sort_frequency_dict(get_ngrams(filtered_tokens, 1)))
