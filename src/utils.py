from typing import Any

from pydantic import BaseModel, HttpUrl
from pydantic_core import Url


class Paper(BaseModel):
    """Pydantic model which stores single paper infomation."""

    title: str
    author: str
    abstract: str
    page: HttpUrl
    pdf: HttpUrl


class PartialPaper(BaseModel):
    """Pydantic model which stores partial paper information."""

    title: str
    author: str
    abstract: str | None = None
    page: HttpUrl | None = None
    pdf: HttpUrl | None = None


def serialize_for_json_dump(object: Any) -> str:
    """Serialize object for JSON dump.

    Args:
        object (Any): Object to serialize.

    """
    # Serialize pydantic Url object to string
    if isinstance(object, Url):
        return str(object)

    raise TypeError(
        f"Object of type {object.__class__.__name__} is not JSON serializable"
    )
