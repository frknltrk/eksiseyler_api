from pydantic import BaseModel
from typing import Optional


class Article(BaseModel):
    article_id: int
    article_url: str
    article_title: str
    cover_image: str
    article_date: Optional[str]
