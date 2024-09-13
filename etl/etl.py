import psycopg  # Replace psycopg2 with psycopg
import logging
import os
import time  # Import time for sleep
from scraper import scrape_articles

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Get database path from environment variable or use default
DATABASE = os.getenv("DATABASE_URL")

# Retry configuration
RETRY_ATTEMPTS = 5
RETRY_DELAY = 5  # seconds

def connect_with_retry():
    for attempt in range(RETRY_ATTEMPTS):
        try:
            conn = psycopg.connect(DATABASE)
            return conn
        except psycopg.Error as e:
            logging.error(f"Attempt {attempt + 1} - Error connecting to database: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise

def setup_database():
    logging.info("Setting up the database.")
    try:
        with connect_with_retry() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS articles (
                                article_id SERIAL PRIMARY KEY,
                                article_url TEXT NOT NULL UNIQUE,
                                article_title TEXT,
                                cover_image TEXT,
                                article_date DATE
                              )"""
                )
                conn.commit()
        logging.info("Database setup complete.")
    except psycopg.Error as e:
        logging.error(f"Error setting up database: {e}")

def count_rows():
    try:
        with connect_with_retry() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM articles")
                count = cursor.fetchone()[0]
                logging.info(f"Total number of rows in 'articles' table: {count}")
                return count
    except psycopg.Error as e:
        logging.error(f"Error counting rows: {e}")
        return 0

def insert_articles(articles):
    logging.info(f"Inserting {len(articles)} articles into the database.")
    try:
        with connect_with_retry() as conn:
            with conn.cursor() as cursor:
                articles_tuples = [
                    (
                        article["article_url"],
                        article["article_title"],
                        article["cover_image"],
                    )
                    for article in articles
                ]
                cursor.executemany(
                    """INSERT INTO articles (article_url, article_title, cover_image) VALUES (%s, %s, %s)""",
                    articles_tuples,
                )
                conn.commit()
        logging.info("Articles inserted successfully.")
    except psycopg.Error as e:
        logging.error(f"Error inserting articles: {e}")

def drop_table():
    logging.info("Dropping the 'articles' table if it exists.")
    try:
        with connect_with_retry() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS articles")
                conn.commit()
        logging.info("'articles' table dropped successfully.")
    except psycopg.Error as e:
        logging.error(f"Error dropping table: {e}")

def run_initial_etl():
    logging.info("Starting initial ETL process.")
    drop_table()  # Drop the table at the beginning
    setup_database()
    try:
        logging.info("Counting rows before insert.")
        count_rows()
        articles = scrape_articles(max_pages=None)  # Fetch all articles initially
    except Exception as e:
        logging.error(f"Initial ETL process failed: {e}")
    else:
        insert_articles(articles)
        logging.info("Counting rows after insert.")
        count_rows()
    logging.info("Initial ETL process completed.")

if __name__ == "__main__":
    # Uncomment the below line to set up the database and run the initial ETL process when the server (cron) starts
    # run_initial_etl()
