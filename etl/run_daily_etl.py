import logging
from etl import scrape_articles, insert_articles

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_daily_etl():
    logging.info("Starting daily ETL process.")
    try:
        articles = scrape_articles(max_pages=1)  # Fetch only the latest articles
        insert_articles(articles)
    except Exception as e:
        logging.error(f"Daily ETL process failed: {e}")
    logging.info("Daily ETL process completed.")


if __name__ == "__main__":
    run_daily_etl()
