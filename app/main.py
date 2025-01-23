import os, datetime, psycopg_pool
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Use connection pooling
POSTGRES_ENDPOINT = os.getenv("POSTGRES_DB_ENDPOINT_URL")
pool = psycopg_pool.ConnectionPool(
    POSTGRES_DB_ENDPOINT_URL,
    min_size=1,  # Minimum connections
    max_size=10,  # Maximum connections
    timeout=10,  # Adjust timeout to handle slow startups
)


class Article(BaseModel):
    article_url: str
    article_title: str
    cover_image: str
    scraped_at: datetime.datetime


def get_db():
    with pool.connection() as conn:
        yield conn


@app.get("/articles/all", response_model=List[Article])
def read_all_articles(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "SELECT article_url, article_title, cover_image, scraped_at FROM articles"
        )
        rows = cur.fetchall()
    return [
        Article(
            article_url=row[0],
            article_title=row[1],
            cover_image=row[2],
            scraped_at=row[3],
        )
        for row in rows
    ]


@app.get("/articles/random", response_model=Article)
def read_random_article(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "SELECT article_url, article_title, cover_image, scraped_at FROM articles ORDER BY RANDOM() LIMIT 1"
        )
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No articles found")
    return Article(
        article_url=row[0], article_title=row[1], cover_image=row[2], scraped_at=row[3]
    )


@app.get("/health")
def health_check():
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
