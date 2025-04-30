from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    url: str
    content: str
    date: datetime
    ticker: str | None = None
    published_at: str | None = None
    source: str | None = None
    system: str | None = None
