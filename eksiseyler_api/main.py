from fastapi import FastAPI, HTTPException
from .models import Article
from typing import List
import random
import sqlite3

app = FastAPI()


def get_articles():
    conn = sqlite3.connect("data/eksiseyler.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT article_id, article_url, article_title, cover_image, article_date FROM articles"
    )
    rows = cursor.fetchall()
    conn.close()
    print(rows[0])
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
    articles = get_articles()
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")
    return random.choice(articles)


@app.get("/articles", response_model=List[Article])
def read_articles():
    return get_articles()


@app.get("/articles/random", response_model=Article)
def read_random_article():
    return get_random_article()
