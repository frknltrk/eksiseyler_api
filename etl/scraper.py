import os, time, logging, requests, psycopg, argparse, datetime
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def scrape_articles(max_pages):
    base_url = "https://eksiseyler.com/"
    load_more_url = "https://eksiseyler.com/Home/PartialLoadMore"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }
    articles = {}
    page = 1
    category_id = 0

    while True:
        if max_pages and page > max_pages:
            break
        logging.info(f"Scraping articles from page {page}")
        try:
            if page == 1:
                response = requests.get(base_url, headers=headers)
            else:
                response = requests.get(
                    load_more_url,
                    headers=headers,
                    params={"PageNumber": page, "CategoryId": category_id},
                )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            divs = soup.find_all("div", class_=["content-img", "mashup-img"])
            if not divs:
                break

            for div in divs:
                url = div.a["href"]
                title = div.img["alt"]
                img = div.img.get("data-src") or div.img.get("src")
                articles[url] = {
                    "article_url": url,
                    "article_title": title,
                    "cover_image": img,
                }

            logging.info(f"Scraped {len(articles)} articles so far.")
            page += 1
            time.sleep(1)
        except requests.RequestException as e:
            logging.error(f"Error scraping articles: {e}")
            break

    logging.info(f"Total articles scraped: {len(articles)}")
    return list(articles.values())


def transform(data):
    for article in data:
        article["scraped_at"] = datetime.datetime.now().isoformat()
    return data


def export_data_to_postgres(data):
    db_url = os.getenv("POSTGRES_DB_ENDPOINT_URL")
    if not db_url:
        raise ValueError("POSTGRES_DB_ENDPOINT_URL environment variable is not set")

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:

            # Upsert articles into the table
            for article in data:
                cur.execute(
                    """
                    INSERT INTO articles (article_url, article_title, cover_image, scraped_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (article_url)
                    DO UPDATE SET
                        article_title = EXCLUDED.article_title,
                        cover_image = EXCLUDED.cover_image,
                        scraped_at = EXCLUDED.scraped_at
                """,
                    (
                        article["article_url"],
                        article["article_title"],
                        article["cover_image"],
                        article["scraped_at"],
                    ),
                )

        logging.info("Data export completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape articles from eksiseyler.com")
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to scrape. Default is 1. Use 0 for all pages.",
        default=1,
    )

    args = parser.parse_args()

    articles = scrape_articles(max_pages=args.max_pages if args.max_pages > 0 else None)
    transformed_data = transform(articles)
    export_data_to_postgres(transformed_data)
