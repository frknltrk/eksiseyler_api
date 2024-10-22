import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import psycopg_pool

app = FastAPI()

# Use connection pooling
DATABASE_URL = os.getenv("DATABASE_URL")
pool = psycopg_pool.ConnectionPool(DATABASE_URL)

class Article(BaseModel):
    article_url: str
    article_title: str
    cover_image: str
    scraped_at: str

def get_db():
    with pool.connection() as conn:
        yield conn

@app.get("/articles/all", response_model=List[Article])
def read_all_articles(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT article_url, article_title, cover_image, scraped_at FROM articles")
        rows = cur.fetchall()
    return [Article(article_url=row[0], article_title=row[1], cover_image=row[2], scraped_at=row[3]) for row in rows]

@app.get("/articles/random", response_model=Article)
def read_random_article(db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT article_url, article_title, cover_image, scraped_at FROM articles ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No articles found")
    return Article(article_url=row[0], article_title=row[1], cover_image=row[2], scraped_at=row[3])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
