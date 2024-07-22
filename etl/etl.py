import sqlite3
from scraper import scrape_articles


def setup_database():
    conn = sqlite3.connect("data/eksiseyler.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS articles (
                    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_url TEXT NOT NULL UNIQUE,
                    article_title TEXT,
                    cover_image TEXT,
                    article_date DATE
                  )"""
    )
    conn.commit()
    conn.close()


def insert_articles(articles):
    conn = sqlite3.connect("data/eksiseyler.db")
    cursor = conn.cursor()
    cursor.executemany(
        """INSERT OR IGNORE INTO articles (article_url, article_title, cover_image)
                      VALUES (?, ?, ?)""",
        reversed(articles),
    )
    conn.commit()
    conn.close()


def run_etl():
    setup_database()
    articles = scrape_articles()
    insert_articles(articles)


if __name__ == "__main__":
    run_etl()
