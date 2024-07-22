from pydantic import BaseModel


class Article(BaseModel):
    article_id: int
    article_url: str
    article_title: str
    cover_image: str
    article_date: str | None
