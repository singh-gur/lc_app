from datetime import datetime

from pydantic import BaseModel
from typing import Generic, TypeVar
T = TypeVar("T")

class Article(BaseModel):
    title: str
    url: str
    content: str
    date: datetime
    ticker: str | None = None
    topic: str | None = None
    published_at: str | None = None
    source: str | None = None
    system: str | None = None


class DataSet(BaseModel, Generic[T]):
    entries: list[T]