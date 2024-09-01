import requests
import logging
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def scrape_articles():
    url = "https://eksiseyler.com/"
    logging.info(f"Scraping articles from {url}")
    try:
        h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
        }
        response = requests.get(url, headers=h)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")
        articles = []

        divs = soup.find_all("div", class_=["content-img", "mashup-img"])

        for div in divs:
            url = div.a["href"]
            title = div.img["alt"]
            img = div.img.get("data-src") or div.img.get(
                "src"
            )  # content-img or mashup-img

            # as tuples:
            articles.insert(0, (url, title, img))
            # as dict items:
            # parsed_dict.append({
            #     'article_url': url,
            #     'article_title': title,
            #     'cover_image': img
            # })

        logging.info(f"Scraped {len(articles)} articles.")
        return articles
    except requests.RequestException as e:
        logging.error(f"Error scraping articles: {e}")
        return []
