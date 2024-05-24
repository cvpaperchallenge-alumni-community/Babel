from typing import cast

import wordcloud


def calculate_word_frequency(text: str) -> dict[str, int]:
    """Calculate word frequencies from the given text. This function is
    considering default stopwords defined in wordcloud.WordCloud.

    Args:
        text (str): Text to calculate word frequencies.

    Returns:
        dict[str, int]: A frequency dict.

    NOTE: Collocations (bigrams) of two words are under consideration.
    Its implementation detail is available at:
    https://github.com/amueller/word_cloud/blob/main/wordcloud/wordcloud.py#L597

    """
    return cast(dict[str, int], wordcloud.WordCloud().process_text(text))


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
    print(calculate_word_frequency(text))
