from fastapi import FastAPI, HTTPException
from .models import Article
from typing import List
import psycopg  # Replace psycopg2 with psycopg
import os

app = FastAPI()

DATABASE = os.getenv("DATABASE_URL")


def get_articles():
    conn = psycopg.connect(DATABASE)  # Update connection
    cursor = conn.cursor()
    cursor.execute(
        "SELECT article_id, article_url, article_title, cover_image, article_date FROM articles"
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        Article(
            article_id=row[0],
            article_url=row[1],
            article_title=row[2],
            cover_image=row[3],
            article_date=row[4],
        )
        for row in rows
    ]


def get_random_article():
    conn = psycopg.connect(DATABASE)  # Update connection
    cursor = conn.cursor()
    cursor.execute(
        "SELECT article_id, article_url, article_title, cover_image, article_date FROM articles ORDER BY RANDOM() LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="No articles found")

    return Article(
        article_id=row[0],
        article_url=row[1],
        article_title=row[2],
        cover_image=row[3],
        article_date=row[4],
    )


@app.get("/articles/all", response_model=List[Article])
def read_articles():
    return get_articles()


@app.get("/articles/random", response_model=Article)
def read_random_article():
    return get_random_article()
