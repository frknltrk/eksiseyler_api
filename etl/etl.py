import sqlite3
import logging
from scraper import scrape_articles

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def setup_database():
    logging.info("Setting up the database.")
    try:
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
        logging.info("Database setup complete.")
    except sqlite3.Error as e:
        logging.error(f"Error setting up database: {e}")
    finally:
        conn.close()


def count_rows():
    try:
        conn = sqlite3.connect("data/eksiseyler.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles")
        count = cursor.fetchone()[0]
        logging.info(f"Total number of rows in 'articles' table: {count}")
        return count
    except sqlite3.Error as e:
        logging.error(f"Error counting rows: {e}")
        return 0
    finally:
        conn.close()


def insert_articles(articles):
    logging.info(f"Inserting {len(articles)} articles into the database.")
    logging.debug(f"Articles to be inserted: {articles}")
    try:
        conn = sqlite3.connect("data/eksiseyler.db")
        cursor = conn.cursor()
        cursor.executemany(
            """INSERT OR IGNORE INTO articles (article_url, article_title, cover_image)
                          VALUES (?, ?, ?)""",
            reversed(articles),
        )
        conn.commit()
        logging.info("Articles inserted successfully.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting articles: {e}")
    finally:
        conn.close()


def run_etl():
    logging.info("Starting ETL process.")
    setup_database()
    try:
        logging.info("Counting rows before insert.")
        count_rows()
        articles = scrape_articles()
        insert_articles(articles)
        logging.info("Counting rows after insert.")
        count_rows()
    except Exception as e:
        logging.error(f"ETL process failed: {e}")
    logging.info("ETL process completed.")


if __name__ == "__main__":
    run_etl()
