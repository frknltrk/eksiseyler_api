import requests
import logging
from bs4 import BeautifulSoup
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def scrape_articles(max_pages=1):
    base_url = "https://eksiseyler.com/"
    load_more_url = "https://eksiseyler.com/Home/PartialLoadMore"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }
    articles = {}
    page = 1
    category_id = 0  # Assuming 0 is the default category ID for all articles

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

            # Find articles on the current page
            divs = soup.find_all("div", class_=["content-img", "mashup-img"])
            if not divs:
                break  # No more articles to load

            for div in divs:
                url = div.a["href"]
                title = div.img["alt"]
                img = div.img.get("data-src") or div.img.get("src")

                # Use dictionary to avoid duplicates
                articles[url] = {
                    "article_url": url,
                    "article_title": title,
                    "cover_image": img,
                }

            logging.info(f"Scraped {len(articles)} articles so far.")
            page += 1
            time.sleep(1)  # Be polite and avoid hammering the server
        except requests.RequestException as e:
            logging.error(f"Error scraping articles: {e}")
            break

    logging.info(f"Total articles scraped: {len(articles)}")
    return list(articles.values())


if __name__ == "__main__":
    articles = scrape_articles(max_pages=5)  # Example: scrape only 5 pages
    # You can now save the articles to a file or process them further
