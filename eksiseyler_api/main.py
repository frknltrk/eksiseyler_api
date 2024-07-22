from fastapi import FastAPI, HTTPException
from .models import Article
from typing import List
import random
import sqlite3

app = FastAPI()

DATABASE = "data/eksiseyler.db"


def get_articles():
    conn = sqlite3.connect(DATABASE)
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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get total count of articles
    cursor.execute("SELECT COUNT(1) FROM articles")
    count = cursor.fetchone()[0]

    if count == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="No articles found")

    # Fetch one random article based on a random rowid
    random_id = random.randint(1, count)
    cursor.execute(
        "SELECT article_id, article_url, article_title, cover_image, article_date FROM articles WHERE rowid = ?",
        (random_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return Article(
        article_id=row[0],
        article_url=row[1],
        article_title=row[2],
        cover_image=row[3],
        article_date=row[4],
    )


@app.get("/articles", response_model=List[Article])
def read_articles():
    return get_articles()


@app.get("/articles/random", response_model=Article)
def read_random_article():
    return get_random_article()
